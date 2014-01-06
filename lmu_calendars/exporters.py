from scrapy.contrib.exporter import BaseItemExporter
from icalendar import Calendar, Event

class ICalendarExporter(BaseItemExporter):
    ics_fields = ['dtstamp', 'uid', 'dtstart', 'class', 'created', 'description',
                  'geo', 'last-mod', 'location', 'organizer', 'priority', 'seq',
                  'status', 'summary', 'transp', 'url', 'recurid', 'rrule',
                  'dtend', 'duration', 'attach', 'attendee', 'categories', 'comment',
                  'contact', 'exdate', 'rstatus', 'related', 'resources', 'rdate']
    
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.encoding = 'utf-8'
        self.file = file

    def _to_str_if_unicode(self, value):
        return value.encode(self.encoding, 'replace') if isinstance(value, unicode) else value
        
    def start_exporting(self):
        self.cal = Calendar()
        self.cal.add('prodid', '-//Kaleo//-//')
        self.cal.add('version', '2.0')
        
    def finish_exporting(self):
        self.file.write(self.cal.to_ical())#.decode('utf-8').encode('utf-8'))

    def export_item(self, item):
        event = Event()
        
        field_iter = set(item.keys())

        for field_name in field_iter:
            if field_name in item:
                field = item.fields[field_name]
                value = self.serialize_field(field, field_name, item[field_name])
            else:
                value = default_value
                        
            if field_name[0] == '_': 
                event.add(field_name[1:].replace('_','-'), value)
            else:
                event.add(field_name.replace('_','-'), value)
                #event.add('attendee', 'mailto:andrew.whitby@me.com')
                #event.add('organizer', 'mailto:test@example.com')
                #event['attendee'].params.update({'CN': 'andrew.whitby@me.com'})
                #event['attendee'].params.update({'RSVP': 'TRUE'})
                #event['attendee'].params.update({'ROLE': 'REQ_PARTICIPANT'})
                #event['attendee'].params.update({'PARTSTAT': 'NEEDS-ACTION'})
        
        self.cal.add_component(event)
