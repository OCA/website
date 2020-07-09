# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from random import randint
import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo import SUPERUSER_ID
from dateutil import tz
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class WebsiteSupportTicket(models.Model):

    _name = "website.support.ticket"
    _description = "Website Support Ticket"
    _order = "create_date desc"
    _rec_name = "subject"
    _inherit = ['mail.thread']
    _translate = True

    @api.model
    def _read_group_state(self, states, domain, order):
        """ Read group customization in order to display all the states in the
            kanban view, even if they are empty
        """

        staff_replied_state = self.env['ir.model.data'].get_object('website_support',
                                                                   'website_ticket_state_staff_replied')
        customer_replied_state = self.env['ir.model.data'].get_object('website_support',
                                                                      'website_ticket_state_customer_replied')
        customer_closed = self.env['ir.model.data'].get_object('website_support',
                                                               'website_ticket_state_customer_closed')
        staff_closed = self.env['ir.model.data'].get_object('website_support', 'website_ticket_state_staff_closed')

        exclude_states = [staff_replied_state.id, customer_replied_state.id, customer_closed.id, staff_closed.id]

        # state_ids = states._search([('id','not in',exclude_states)], order=order, access_rights_uid=SUPERUSER_ID)
        state_ids = states._search([], order=order, access_rights_uid=SUPERUSER_ID)

        return states.browse(state_ids)

    def _default_state(self):
        return self.env['ir.model.data'].get_object('website_support', 'website_ticket_state_open')

    def _default_priority_id(self):
        default_priority = self.env['website.support.ticket.priority'].search([('sequence','=','1')])
        return default_priority[0]

    def _default_approval_id(self):
        return self.env['ir.model.data'].get_object('website_support', 'no_approval_required')

    channel = fields.Char(string="Channel", default="Manual")
    create_user_id = fields.Many2one('res.users', "Create User")
    priority_id = fields.Many2one('website.support.ticket.priority', default=_default_priority_id, string="Priority")
    parent_company_id = fields.Many2one(string="Parent Company", related="partner_id.company_id")
    partner_id = fields.Many2one('res.partner', string="Partner")
    user_id = fields.Many2one('res.users', string="Assigned User")
    person_name = fields.Char(string='Person Name')
    email = fields.Char(string="Email")
    support_email = fields.Char(string="Support Email")
    category_id = fields.Many2one('website.support.ticket.category', string="Category", track_visibility='onchange')
    sub_category_id = fields.Many2one('website.support.ticket.subcategory', string="Sub Category")
    subject = fields.Char(string="Subject")
    description = fields.Text(string="Description")
    state_id = fields.Many2one('website.support.ticket.state', group_expand='_read_group_state', default=_default_state,
                            string="State")
    conversation_history_ids = fields.One2many('website.support.ticket.message', 'ticket_id', string="Conversation History")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'website.support.ticket')],
                                     string="Media Attachments")
    unattended = fields.Boolean(string="Unattended", compute="_compute_unattend", store="True",
                                help="In 'Open' state or 'Customer Replied' state taken into consideration name changes")
    portal_access_key = fields.Char(string="Portal Access Key")
    ticket_number = fields.Char(string="Ticket Number", readonly=True)
    ticket_color = fields.Char(related="priority_id.color", string="Ticket Color")
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env['res.company']._company_default_get('website.support.ticket') )
    support_rating = fields.Integer(string="Support Rating")
    support_comment = fields.Text(string="Support Comment")
    close_comment = fields.Html(string="Close Comment")
    close_time = fields.Datetime(string="Close Time")
    close_date = fields.Date(string="Close Date")
    closed_by_id = fields.Many2one('res.users', string="Closed By")
    time_to_close = fields.Integer(string="Time to close (seconds)")
    extra_field_ids = fields.One2many('website.support.ticket.field', 'wst_id', string="Extra Details")
    planned_time = fields.Datetime(string="Planned Time")
    planned_time_format = fields.Char(string="Planned Time Format", compute="_compute_planned_time_format")
    approval_id = fields.Many2one('website.support.ticket.approval', default=_default_approval_id, string="Approval")
    approval_message = fields.Text(string="Approval Message")
    approve_url = fields.Char(compute="_compute_approve_url", string="Approve URL")
    disapprove_url = fields.Char(compute="_compute_disapprove_url", string="Disapprove URL")
    tag_ids = fields.Many2many('website.support.ticket.tag', string="Tags")
    sla_id = fields.Many2one('website.support.sla', string="SLA")
    sla_timer = fields.Float(string="SLA Time Remaining")
    sla_timer_format = fields.Char(string="SLA Timer Format", compute="_compute_sla_timer_format")
    sla_active = fields.Boolean(string="SLA Active")
    sla_rule_id = fields.Many2one('website.support.sla.rule', string="SLA Rule")
    sla_alert_ids = fields.Many2many('website.support.sla.alert', string="SLA Alerts",
                                     help="Keep record of SLA alerts sent so we do not resend them")

    @api.one
    @api.depends('sla_timer')
    def _compute_sla_timer_format(self):
        # Display negative hours in a positive format
        self.sla_timer_format = '{0:02.0f}:{1:02.0f}'.format(*divmod(abs(self.sla_timer) * 60, 60))

    @api.model
    def update_sla_timer(self):

        # Subtract 1 minute from the timer of all active SLA tickets, this includes going into negative
        for active_sla_ticket in self.env['website.support.ticket'].search([('sla_active','=',True),('sla_id','!=',False),('sla_rule_id','!=',False)]):

            # If we only countdown during busines hours
            if active_sla_ticket.sla_rule_id.countdown_condition == 'business_only':
                # Check if the current time aligns with a timeslot in the settings,
                # setting has to be set for business_only or UserError occurs
                setting_business_hours_id = self.env['ir.default'].get('website.support.settings', 'business_hours_id')
                current_hour = datetime.datetime.now().hour
                current_minute = datetime.datetime.now().minute / 60
                current_hour_float = current_hour + current_minute
                day_of_week = datetime.datetime.now().weekday()
                during_work_hours = self.env['resource.calendar.attendance'].search([('calendar_id','=', setting_business_hours_id), ('dayofweek','=',day_of_week), ('hour_from','<',current_hour_float), ('hour_to','>',current_hour_float)])

                # If holiday module is installed take into consideration
                holiday_module = self.env['ir.module.module'].search([('name','=','hr_public_holidays'), ('state','=','installed')])
                if holiday_module:
                    holiday_today = self.env['hr.holidays.public.line'].search([('date','=',datetime.datetime.now().date())])
                    if holiday_today:
                        during_work_hours = False

                if during_work_hours:
                    active_sla_ticket.sla_timer -= 1/60
            elif active_sla_ticket.sla_rule_id.countdown_condition == '24_hour':
                #Countdown even if the business hours setting is not set
                active_sla_ticket.sla_timer -= 1/60

            #Send an email out to everyone in the category about the SLA alert
            notification_template = self.env['ir.model.data'].sudo().get_object('website_support', 'support_ticket_sla_alert')

            for sla_alert in self.env['website.support.sla.alert'].search([('vsa_id','=',active_sla_ticket.sla_id.id), ('alert_time','>=', active_sla_ticket.sla_timer)]):

                #Only send out the alert once
                if sla_alert not in active_sla_ticket.sla_alert_ids:

                    for my_user in active_sla_ticket.category_id.cat_user_ids:
                        values = notification_template.generate_email(active_sla_ticket.id)
                        values['body_html'] = values['body_html'].replace("_user_name_",  my_user.partner_id.name)
                        values['email_to'] = my_user.partner_id.email

                        send_mail = self.env['mail.mail'].create(values)
                        send_mail.send()

                        #Remove the message from the chatter since this would bloat the communication history by a lot
                        send_mail.mail_message_id.res_id = 0

                    #Add the alert to the list of already sent SLA
                    active_sla_ticket.sla_alert_ids = [(4, sla_alert.id)]

    def pause_sla(self):
        self.sla_active = False

    def resume_sla(self):
        self.sla_active = True

    @api.one
    @api.depends('planned_time')
    def _compute_planned_time_format(self):

        #If it is assigned to the partner, use the partners timezone and date formatting
        if self.planned_time and self.partner_id and self.partner_id.lang:
            partner_language = self.env['res.lang'].search([('code','=', self.partner_id.lang)])[0]

            #If we have timezone information translate the planned date to local time otherwise UTC
            if self.partner_id.tz:
                my_planned_time = self.planned_time.replace(tzinfo=tz.gettz('UTC'))
                local_time = my_planned_time.astimezone(tz.gettz(self.partner_id.tz))
                self.planned_time_format = local_time.strftime(partner_language.date_format + " " + partner_language.time_format) + " " + self.partner_id.tz
            else:
                self.planned_time_format = self.planned_time.strftime(partner_language.date_format + " " + partner_language.time_format) + " UTC"

        else:
            self.planned_time_format = self.planned_time

    @api.one
    def _compute_approve_url(self):
        self.approve_url = "/support/approve/" + str(self.id)

    @api.one
    def _compute_disapprove_url(self):
        self.disapprove_url = "/support/disapprove/" + str(self.id)

    @api.onchange('category')
    def _onchange_category(self):
        self.sub_category_id = False

    @api.onchange('sub_category_id')
    def _onchange_sub_category_id(self):
        if self.sub_category_id:

            add_extra_fields = []

            for extra_field in self.sub_category_id.additional_field_ids:
                add_extra_fields.append((0, 0, {'name': extra_field.name}))

            self.update({
                'extra_field_ids': add_extra_fields,
            })

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.person_name = self.partner_id.name
        self.email = self.partner_id.email

    def message_new(self, msg, custom_values=None):
        """ Create new support ticket upon receiving new email"""

        defaults = {'support_email': msg.get('to'), 'subject': msg.get('subject')}

        #Extract the name from the from email if you can
        if "<" in msg.get('from') and ">" in msg.get('from'):
            start = msg.get('from').rindex( "<" ) + 1
            end = msg.get('from').rindex( ">", start )
            from_email = msg.get('from')[start:end]
            from_name = msg.get('from').split("<")[0].strip()
            defaults['person_name'] = from_name
        else:
            from_email = msg.get('from')

        defaults['email'] = from_email
        defaults['channel'] = "Email"

        #Try to find the partner using the from email
        search_partner = self.env['res.partner'].sudo().search([('email','=', from_email)])
        if len(search_partner) > 0:
            defaults['partner_id'] = search_partner[0].id
            defaults['person_name'] = search_partner[0].name

        defaults['description'] = tools.html_sanitize(msg.get('body'))

        #Assign to default category
        setting_email_default_category_id = self.env['ir.default'].get('website.support.settings', 'email_default_category_id')

        if setting_email_default_category_id:
            defaults['category_id'] = setting_email_default_category_id

        return super(WebsiteSupportTicket, self).message_new(msg, custom_values=defaults)

    def message_update(self, msg_dict, update_vals=None):
        """ Override to update the support ticket according to the email. """

        body_short = tools.html_sanitize(msg_dict['body'])

        #If the to email address is to the customer then it must be a staff member
        if msg_dict.get('to') == self.email:
            change_state = self.env['ir.model.data'].get_object('website_support','website_ticket_state_staff_replied')
        else:
            change_state = self.env['ir.model.data'].get_object('website_support','website_ticket_state_customer_replied')

        self.state_id = change_state.id

        #Add to message history to keep HTML clean
        self.conversation_history_ids.create({'ticket_id': self.id, 'by': 'customer', 'content': body_short })

        return super(WebsiteSupportTicket, self).message_update(msg_dict, update_vals=update_vals)

    @api.one
    @api.depends('state_id')
    def _compute_unattend(self):

        if self.state_id.unattended == True:
            self.unattended = True

    @api.multi
    def request_approval(self):

        approval_email = self.env['ir.model.data'].get_object('website_support', 'support_ticket_approval')

        values = self.env['mail.compose.message'].generate_email_for_composer(approval_email.id, [self.id])[self.id]

        request_message = values['body']

        return {
            'name': "Request Approval",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'website.support.ticket.compose',
            'context': {'default_ticket_id': self.id, 'default_email': self.email, 'default_subject': self.subject, 'default_approval': True, 'default_body': request_message},
            'target': 'new'
        }

    @api.multi
    def open_close_ticket_wizard(self):

        return {
            'name': "Close Support Ticket",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'website.support.ticket.close',
            'context': {'default_ticket_id': self.id},
            'target': 'new'
        }

    @api.model
    def _needaction_domain_get(self):
        open_state = self.env['ir.model.data'].get_object('website_support', 'website_ticket_state_open')
        custom_replied_state = self.env['ir.model.data'].get_object('website_support', 'website_ticket_state_customer_replied')
        return ['|',('state', '=', open_state.id ), ('state_id', '=', custom_replied_state.id)]

    @api.model
    def create(self, vals):
        # Get next ticket number from the sequence
        vals['ticket_number'] = self.env['ir.sequence'].next_by_code('website.support.ticket')

        new_id = super(WebsiteSupportTicket, self).create(vals)

        new_id.portal_access_key = randint(1000000000,2000000000)

        #If the customer has a dedicated support user then automatically assign them
        if new_id.partner_id.dedicated_support_user_id:
            new_id.user_id = new_id.partner_id.dedicated_support_user_id.id

        #Check if this contact has a SLA assigned
        if new_id.partner_id.sla_id:
            
            #Go through all rules starting from the lowest response time
            for sla_rule in new_id.partner_id.sla_id.rule_ids:
                #All conditions have to match
                _logger.error(sla_rule.name)
                all_true = True
                for sla_rule_con in sla_rule.condition_ids:
                    if sla_rule_con.type == "category" and new_id.category_id.id != sla_rule_con.category_id.id:
                        all_true = False
                    elif sla_rule_con.type == "subcategory" and new_id.sub_category_id.id != sla_rule_con.subcategory_id.id:
                        all_true = False
                    elif sla_rule_con.type == "priority" and new_id.priority_id.id != sla_rule_con.priority_id.id:
                        all_true = False
                
                if all_true:
                    new_id.sla_id = new_id.partner_id.sla_id.id
                    new_id.sla_active = True
                    new_id.sla_timer = sla_rule.response_time
                    new_id.sla_rule_id = sla_rule.id
                    break

        ticket_open_email_template = self.env['ir.model.data'].get_object('website_support', 'website_ticket_state_open').mail_template_id
        ticket_open_email_template.send_mail(new_id.id, True)

        #Send an email out to everyone in the category
        notification_template = self.env['ir.model.data'].sudo().get_object('website_support', 'new_support_ticket_category')
        support_ticket_menu = self.env['ir.model.data'].sudo().get_object('website_support', 'website_support_ticket_menu')
        support_ticket_action = self.env['ir.model.data'].sudo().get_object('website_support', 'website_support_ticket_action')

        #Add them as a follower to the ticket so they are aware of any internal notes
        partner_ids = []
        for u in new_id.category_id.cat_user_ids:
            partner_ids.append(u.partner_id.id)
        new_id.message_subscribe(partner_ids=partner_ids)

        for my_user in new_id.category_id.cat_user_ids:
            values = notification_template.generate_email(new_id.id)
            values['body_html'] = values['body_html'].replace("_ticket_url_", request.httprequest.host_url + "web#id=" + str(new_id.id) + "&view_type=form&model=website.support.ticket&menu_id=" + str(support_ticket_menu.id) + "&action=" + str(support_ticket_action.id) ).replace("_user_name_",  my_user.partner_id.name)
            values['email_to'] = my_user.partner_id.email

            send_mail = self.env['mail.mail'].create(values)
            send_mail.send()

            #Remove the message from the chatter since this would bloat the communication history by a lot
            send_mail.mail_message_id.res_id = 0

        return new_id

    @api.multi
    def write(self, values, context=None):

        update_rec = super(WebsiteSupportTicket, self).write(values)

        if 'state_id' in values:
            if self.state_id.mail_template_id:
                self.state_id.mail_template_id.send_mail(self.id, True)

        #Email user if category has changed
        if 'category_id' in values:
            change_category_email = self.env['ir.model.data'].sudo().get_object('website_support', 'new_support_ticket_category_change')
            change_category_email.send_mail(self.id, True)

        if 'user_id' in values:
            setting_change_user_email_template_id = self.env['ir.default'].get('website.support.settings', 'change_user_email_template_id')

            if setting_change_user_email_template_id:
                email_template = self.env['mail.template'].browse(setting_change_user_email_template_id)
            else:
                #Default email template
                email_template = self.env['ir.model.data'].get_object('website_support','support_ticket_user_change')

            email_values = email_template.generate_email([self.id])[self.id]
            email_values['model'] = "website.support.ticket"
            email_values['res_id'] = self.id
            assigned_user = self.env['res.users'].browse( int(values['user_id']) )
            email_values['email_to'] = assigned_user.partner_id.email
            email_values['body_html'] = email_values['body_html'].replace("_user_name_", assigned_user.name)
            email_values['body'] = email_values['body'].replace("_user_name_", assigned_user.name)
            send_mail = self.env['mail.mail'].create(email_values)
            send_mail.send()


        return update_rec

    def send_survey(self):
        notification_template = self.env['ir.model.data'].sudo().get_object('website_support', 'support_ticket_survey')
        values = notification_template.generate_email(self.id)
        send_mail = self.env['mail.mail'].create(values)
        send_mail.send(True)

class WebsiteSupportTicketApproval(models.Model):

    _name = "website.support.ticket.approval"

    wst_id = fields.Many2one('website.support.ticket', string="Support Ticket")
    name = fields.Char(string="Name", translate=True)

class WebsiteSupportTicketField(models.Model):

    _name = "website.support.ticket.field"

    wst_id = fields.Many2one('website.support.ticket', string="Support Ticket")
    name = fields.Char(string="Label")
    value = fields.Char(string="Value")

class WebsiteSupportTicketMessage(models.Model):

    _name = "website.support.ticket.message"

    ticket_id = fields.Many2one('website.support.ticket', string='Ticket ID')
    by = fields.Selection([('staff','Staff'), ('customer','Customer')], string="By")
    content = fields.Html(string="Content")

    @api.model
    def create(self, values):

        new_record = super(WebsiteSupportTicketMessage, self).create(values)
        
        # Notify everyone following the ticket of the custoemr reply
        if values['by'] == "customer":
            customer_reply_email_template = self.env['ir.model.data'].get_object('website_support','support_ticket_customer_reply_wrapper')
            email_values = customer_reply_email_template.generate_email(new_record.id)
            for follower in new_record.ticket_id.message_follower_ids:
                email_values['email_to'] = follower.partner_id.email
                send_mail = self.env['mail.mail'].sudo().create(email_values)
                send_mail.send()

        return new_record

class WebsiteSupportTicketCategory(models.Model):

    _name = "website.support.ticket.category"
    _order = "sequence asc"

    sequence = fields.Integer(string="Sequence")
    name = fields.Char(required=True, translate=True, string='Category Name')
    cat_user_ids = fields.Many2many('res.users', string="Category Users")
    access_group_ids = fields.Many2many('res.groups', string="Access Groups", help="Restrict which users can select the category on the website form, none = everyone")

    @api.model
    def create(self, values):
        sequence=self.env['ir.sequence'].next_by_code('website.support.ticket.category')
        values['sequence']=sequence
        return super(WebsiteSupportTicketCategory, self).create(values)

class WebsiteSupportTicketSubCategory(models.Model):

    _name = "website.support.ticket.subcategory"
    _order = "sequence asc"

    sequence = fields.Integer(string="Sequence")
    name = fields.Char(required=True, translate=True, string='Sub Category Name')
    parent_category_id = fields.Many2one('website.support.ticket.category', required=True, string="Parent Category")
    additional_field_ids = fields.One2many('website.support.ticket.subcategory.field', 'wsts_id', string="Additional Fields")

    @api.model
    def create(self, values):
        sequence=self.env['ir.sequence'].next_by_code('website.support.ticket.subcategory')
        values['sequence']=sequence
        return super(WebsiteSupportTicketSubCategory, self).create(values)

class WebsiteSupportTicketSubCategoryField(models.Model):

    _name = "website.support.ticket.subcategory.field"

    wsts_id = fields.Many2one('website.support.ticket.subcategory', string="Sub Category")
    name = fields.Char(string="Label", required="True")
    type = fields.Selection([('textbox','Textbox'),('dropbox','Dropbox')], default="textbox", required="True", string="Type")
    dropbox_type = fields.Selection([('static','Static')], default="static", string="Dropbox Type")
    value_ids = fields.One2many('website.support.ticket.subcategory.field.value', 'wstsf_id', string="Values")

class WebsiteSupportTicketSubCategoryFieldValue(models.Model):

    _name = "website.support.ticket.subcategory.field.value"

    wstsf_id = fields.Many2one('website.support.ticket.subcategory.field', string="Subcategory Field")
    name = fields.Char(string="Name")

class WebsiteSupportTicketState(models.Model):

    _name = "website.support.ticket.state"

    name = fields.Char(required=True, translate=True, string='State Name')
    mail_template_id = fields.Many2one('mail.template', domain="[('model_id','=','website.support.ticket')]", string="Mail Template", help="The mail message that the customer gets when the state changes")
    unattended = fields.Boolean(string="Unattended", help="If ticked, tickets in this state will appear by default")

class WebsiteSupportTicketPriority(models.Model):

    _name = "website.support.ticket.priority"
    _order = "sequence asc"

    sequence = fields.Integer(string="Sequence")
    name = fields.Char(required=True, translate=True, string="Priority Name")
    color = fields.Char(string="Color")

    @api.model
    def create(self, values):
        sequence=self.env['ir.sequence'].next_by_code('website.support.ticket.priority')
        values['sequence']=sequence
        return super(WebsiteSupportTicketPriority, self).create(values)

class WebsiteSupportTicketTag(models.Model):

    _name = "website.support.ticket.tag"

    name = fields.Char(required=True, translate=True, string="Tag Name")

class WebsiteSupportTicketUsers(models.Model):

    _inherit = "res.users"

    cat_user_ids = fields.Many2many('website.support.ticket.category', string="Category Users")

class WebsiteSupportTicketClose(models.TransientModel):

    _name = "website.support.ticket.close"

    ticket_id = fields.Many2one('website.support.ticket', string="Ticket ID")
    message = fields.Html(string="Close Message", required=True)
    template_id = fields.Many2one('mail.template', string="Mail Template", domain="[('model_id','=','website.support.ticket'), ('built_in','=',False)]")

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            values = self.env['mail.compose.message'].generate_email_for_composer(self.template_id.id, [self.ticket_id.id])[self.ticket_id.id]
            self.message = values['body']

    def close_ticket(self):

        self.ticket_id.close_time = datetime.datetime.now()

        #Also set the date for gamification
        self.ticket_id.close_date = datetime.date.today()

        diff_time = self.ticket_id.close_time - self.ticket_id.create_date
        self.ticket_id.time_to_close = diff_time.seconds

        closed_state = self.env['ir.model.data'].sudo().get_object('website_support', 'website_ticket_state_staff_closed')

        #We record state change manually since it would spam the chatter if every 'Staff Replied' and 'Customer Replied' gets recorded
        message = "<ul class=\"o_mail_thread_message_tracking\">\n<li>State:<span> " + self.ticket_id.state_id.name + " </span><b>-></b> " + closed_state.name + " </span></li></ul>"
        self.ticket_id.message_post(body=message, subject="Ticket Closed by Staff")

        self.ticket_id.close_comment = self.message
        self.ticket_id.closed_by_id = self.env.user.id
        self.ticket_id.state_id = closed_state.id

        self.ticket_id.sla_active = False

        #Auto send out survey
        setting_auto_send_survey = self.env['ir.default'].get('website.support.settings', 'auto_send_survey')
        if setting_auto_send_survey:
            self.ticket_id.send_survey()

class WebsiteSupportTicketCompose(models.Model):

    _name = "website.support.ticket.compose"

    ticket_id = fields.Many2one('website.support.ticket', string='Ticket ID')
    partner_id = fields.Many2one('res.partner', string="Partner", readonly="True")
    email = fields.Char(string="Email", readonly="True")
    subject = fields.Char(string="Subject", readonly="True")
    body = fields.Text(string="Message Body")
    template_id = fields.Many2one('mail.template', string="Mail Template", domain="[('model_id','=','website.support.ticket'), ('built_in','=',False)]")
    approval = fields.Boolean(string="Approval")
    planned_time = fields.Datetime(string="Planned Time")

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            values = self.env['mail.compose.message'].generate_email_for_composer(self.template_id.id, [self.ticket_id.id])[self.ticket_id.id]
            self.body = values['body']

    @api.one
    def send_reply(self):

        #Change the approval state before we send the mail
        if self.approval:
            #Change the ticket state to awaiting approval
            awaiting_approval_state = self.env['ir.model.data'].get_object('website_support','website_ticket_state_awaiting_approval')
            self.ticket_id.state_id = awaiting_approval_state.id

            #One support request per ticket...
            self.ticket_id.planned_time = self.planned_time
            self.ticket_id.approval_message = self.body
            self.ticket_id.sla_active = False

        #Send email
        values = {}

        setting_staff_reply_email_template_id = self.env['ir.default'].get('website.support.settings', 'staff_reply_email_template_id')

        if setting_staff_reply_email_template_id:
            email_wrapper = self.env['mail.template'].browse(setting_staff_reply_email_template_id)

        values = email_wrapper.generate_email([self.id])[self.id]
        values['model'] = "website.support.ticket"
        values['res_id'] = self.ticket_id.id
        send_mail = self.env['mail.mail'].create(values)
        send_mail.send()

        #Add to the message history to keep the data clean from the rest HTML
        self.env['website.support.ticket.message'].create({'ticket_id': self.ticket_id.id, 'by': 'staff', 'content':self.body.replace("<p>","").replace("</p>","")})

        #Post in message history
        #self.ticket_id.message_post(body=self.body, subject=self.subject, message_type='comment', subtype='mt_comment')

        if self.approval:
            #Also change the approval
            awaiting_approval = self.env['ir.model.data'].get_object('website_support','awaiting_approval')
            self.ticket_id.approval_id = awaiting_approval.id
        else:
            #Change the ticket state to staff replied
            staff_replied = self.env['ir.model.data'].get_object('website_support','website_ticket_state_staff_replied')
            self.ticket_id.state_id = staff_replied.id