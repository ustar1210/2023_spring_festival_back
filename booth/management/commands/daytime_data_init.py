from django.core.management import BaseCommand
from booth.models import Booth
import openpyxl
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        excel_file = "C:/Users/USER/Desktop/DaytimeBooth.xlsx"
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb['Sheet1']

        for i in range(2,26):
            row = sheet[i]
            name=row[0].value
            start_end_dates=row[1].value
            location=row[2].value
            type=row[3].value
            start_at, end_at = self.parse_start_end_dates(start_end_dates)
            error=False

            if not error:
                try:
                    booth=Booth.objects.get(name=name)
                    booth.name=name
                    booth.start_at=start_at
                    booth.end_at=end_at
                    booth.location=location
                    booth.type=type
                    booth.save()
                    print(f"{name} 주간부스(학교부스,외부부스) 수정 완료")
                except Booth.DoesNotExist:
                        booth = Booth.objects.create(
                            name=name,
                            start_at=start_at,
                            end_at=end_at,
                            location=location,
                            type=type,
                        )
                        booth.save() 
                        print(f"{name} 주간부스(학교부스,외부부스) 생성 완료")       

    def parse_start_end_dates(self,date_range):
        date_range = str(date_range)
        if '-' in date_range:
            start_date, end_date = date_range.split('-')
            start_at = self.parse_date(start_date.strip())
            end_at = self.parse_date(end_date.strip())
        else:
            start_at = self.parse_date(date_range.strip())
            end_at = start_at
        return start_at, end_at

    def parse_date(self,date_str):
        try:
            date = datetime.strptime(date_str, '%m.%d').replace(year=datetime.now().year)
        except:
            print(f"{date_str}이상함")
        return date

    def location_in_choices(self,location):
        LOCATION_CHOICES = [choice[0] for choice in Booth.LOCATION_CHOICES]
        return location in LOCATION_CHOICES
    
    def type_in_choices(self,type):
        TYPE_CHOICES = [choice[0] for choice in Booth.TYPE_CHOICES]
        return type in TYPE_CHOICES