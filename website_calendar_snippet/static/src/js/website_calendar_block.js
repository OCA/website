(function () {
    'use strict';
    var website = openerp.website;
    var _t = openerp._t;

    website.ready().then(function () {
        website.if_dom_contains('div.calendar_block', function ($el) {
            var $calendar = $el.find('.calendar');
            $calendar.html('');
            var datejs_locale = "/web/static/lib/datejs/globalization/" + $('html').attr('lang').replace("_", "-") + ".js";

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

            $.getScript(datejs_locale, function(data) {
                var shortTimeformat = Date.CultureInfo.formatPatterns.shortTime;
                var dateFormat = Date.CultureInfo.formatPatterns.shortDate;
                console.log(dateFormat);
                $calendar.fullCalendar({
                    events: function(start, end, callback) {
                        $.ajax({
                            url: '/calendar_block/get_events/' + Math.round(start.getTime() / 1000) + '/' + Math.round(end.getTime() / 1000),
                            dataType: 'json',
                            success: function(result) {
                                //Setup colors
                                all_filters[0] = get_color(result.contacts[0]);
                                all_filters[-1] = get_color(-1);
                                _.each(result.contacts, function (c) {
                                    if (!all_filters[c] && c != result.contacts[0]) {
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
                                        if (all_filters[events[i].color] !== undefined) {
                                            events[i].className = 'calendar_color_' + all_filters[events[i].color];
                                        }
                                        else  {
                                            events[i].className = 'cal_opacity calendar_color_'+ all_filters[-1];
                                        }                                        
                                    }
                                }
                                callback(events);
                            }
                        });
                    },   
                    weekNumberTitle: _t("W"),
                    allDayText: _t('All day'), 
                    buttonText : {
                        today: _t("Today"),
                        month: _t("Month"),
                        week: _t("Week"),
                        day: _t("Day")
                    },
                    aspectRatio: 1.8,
                    snapMinutes: 15,
                    weekMode : 'liquid',
                    columnFormat: {
                        month: 'ddd',
                        week: 'ddd ' + dateFormat,
                        day: 'dddd ' + dateFormat,
                    },
                    titleFormat: {
                        month: 'MMMM yyyy',
                        week: dateFormat + "{ '&#8212;'"+ dateFormat,
                        day: dateFormat,
                    },
                    timeFormat : {
                       // for agendaWeek and agendaDay               
                       agenda: shortTimeformat + '{ - ' + shortTimeformat + '}', // 5:00 - 6:30
                        // for all other views
                        '': shortTimeformat.replace(/:mm/,'(:mm)')  // 7pm
                    },
                    axisFormat : shortTimeformat.replace(/:mm/,'(:mm)'),
                    weekNumbers: true,
                    monthNames: Date.CultureInfo.monthNames,
                    monthNamesShort: Date.CultureInfo.abbreviatedMonthNames,
                    dayNames: Date.CultureInfo.dayNames,
                    dayNamesShort: Date.CultureInfo.abbreviatedDayNames,
                    firstDay: Date.CultureInfo.firstDayOfWeek,
                    header: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'month,agendaWeek,agendaDay'
                    },
                    eventAfterRender: function (event, element, view) {
                        if ((view.name !== 'month') && (((event.end-event.start)/60000)<=30)) {
                            //if duration is too small, we see the html code of img
                            var current_title = $(element.find('.fc-event-time')).text();
                            var new_title = current_title.substr(0,current_title.indexOf("<img")>0?current_title.indexOf("<img"):current_title.length);
                            element.find('.fc-event-time').html(new_title);
                        }
                    },
                    eventRender: function (event, element, view) {
                        element.find('.fc-event-title').html(event.title);
                    },
                });      
            });
        });
    });
}());
