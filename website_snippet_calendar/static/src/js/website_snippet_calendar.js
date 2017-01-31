/* Copyright 2017 Onestein
* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

odoo.define('website_snippet_calendar', function(require) {
'use strict';

    var core = require('web.core'),
        time = require('web.time'),
        base = require('web_editor.base'),
        _t = core._t;

    base.ready().done(function() {
        //Reset
        var $calendar = $('.s_calendar .calendar');
        $calendar.html('');

        //Colors
        var all_filters = {};
        var color_map = {};

        var get_color = function(key) {
            if (color_map[key]) {
                return color_map[key];
            }
            var index = (((_.keys(color_map).length + 1) * 5) % 24) + 1;
            color_map[key] = index;
            return index;
        }

        //Get date format
        var dateFormat = time.strftime_to_moment_format(_t.database.parameters.date_format);

        var conversions = [['YYYY', 'yyyy'], ['YY', 'y'], ['DDDD', 'dddd'], ['DD', 'dd']];
        _.each(conversions, function(conv) {
            dateFormat = dateFormat.replace(conv[0], conv[1]);
        });

        $calendar.fullCalendar({
            events: function(start, end, callback) {
                $.ajax({
                    url: '/calendar_snippet/get_events/' + Math.round(start.getTime() / 1000) + '/' + Math.round(end.getTime() / 1000),
                    dataType: 'json',
                    success: function(result) {
                        //Setup colors
                        all_filters[0] = get_color(result.contacts[0]);
                        all_filters[-1] = get_color(-1);
                        _.each(result.contacts, function (c) {
                            if (!all_filters[c]) {
                                all_filters[c] = get_color(c);
                            }
                        });

                        //Mutate data for calendar
                        var events = result.events;
                        for(var i = 0; i < events.length; i++) {
                            events[i].start = Date.parseExact(events[i].start, "yyyy-MM-dd HH:mm:ss");
                            events[i].end = Date.parseExact(events[i].end, "yyyy-MM-dd HH:mm:ss");
                            var start_offset = events[i].start.getTimezoneOffset();
                            var end_offset = events[i].end.getTimezoneOffset();
                            start_offset = start_offset - (start_offset * 2);
                            end_offset = end_offset - (end_offset * 2);
                            events[i].start.addMinutes(start_offset);
                            events[i].end.addMinutes(end_offset);

                            for(var j = 0; j < events[i].attendees.length; j++) {
                                events[i].title += '<img title="' + events[i].attendees[j].name + '" class="attendee_head" src="/web/binary/image?model=res.partner&field=image_small&id=' + events[i].attendees[j].id + '" />';
                            }

                            if (all_filters[events[i].color] !== undefined) {
                                events[i].className = 'calendar_color_'+ all_filters[events[i].color];
                            }
                            else  {
                                events[i].className = 'calendar_color_'+ all_filters[-1];
                            }
                        }
                        callback(events);
                    }
                });
            },
            weekNumberTitle: _t("W"),
            allDayText: _t('All day'),
            monthNames: moment.months(),
            monthNamesShort: moment.monthsShort(),
            dayNames: moment.weekdays(),
            dayNamesShort: moment.weekdaysShort(),
            firstDay: moment._locale._week.dow,
            weekNumberCalculation: function(date) {
                return moment(date).week();
            },
            weekNumbers: true,
            titleFormat: {
                month: 'MMMM yyyy',
                week: "w",
                day: dateFormat,
            },
            titleFormat: {
                month: 'MMMM yyyy',
                week: "w",
                day: dateFormat,
            },
            columnFormat: {
                month: 'ddd',
                week: 'ddd ' + dateFormat,
                day: 'dddd ' + dateFormat,
            },
            weekMode : 'liquid',
            snapMinutes: 15,
            buttonText: {
                today: _t("Today"),
                month: _t("Month"),
                week: _t("Week"),
                day: _t("Day")
            },
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            eventAfterRender: function (event, element, view) {
                if ((view.name !== 'month') && (((event.end-event.start)/60000) <= 30)) {
                    //if duration is too small, we see the html code of img
                    var current_title = $(element.find('.fc-event-time')).text();
                    var new_title = current_title.substr(0,current_title.indexOf("<img") > 0 ? current_title.indexOf("<img") : current_title.length);
                    element.find('.fc-event-time').html(new_title);
                }
            },
            eventRender: function (event, element, view) {
                element.find('.fc-event-title').html(event.title);
            },
        });
    });
});
