from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from booth.models import Booth
import openpyxl, os, json, re
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        excel_file = "C:/Users/USER/Desktop/FoodTruck.xlsx"
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb['Sheet1']

        for i in range(2,15):
            row = sheet[i]
            name=row[0].value
            menu_price=row[1].value
            description=row[2].value
            location=row[3].value
            start_end_dates=row[4].value
            start_at, end_at = self.parse_start_end_dates(start_end_dates)
            error=False

            if not error:
                try:
                    booth=Booth.objects.get(name=name)
                    booth.name=name

                    menu_dict = {}
                    menu_items = menu_price.split(",")
                    for menu_item in menu_items:
                        match = re.match(r"(.+):(\d+)", menu_item)
                        if match:
                            menu_name = match.group(1)
                            price = int(match.group(2))
                            menu_dict[menu_name] = price

                    booth.menu = menu_dict

                    booth.description = description
                    booth.location=location
                    booth.start_at=start_at
                    booth.end_at=end_at
                    booth.save()
                    print(f"{name} 푸드트럭 수정 완료")
                except Booth.DoesNotExist:
                        menu_dict = {}

                        menu_items = menu_price.split(",")
                        for menu_item in menu_items:
                            match = re.match(r"(.+):(\d+)", menu_item)
                            if match:
                                menu_name = match.group(1)
                                price = int(match.group(2))
                                menu_dict[menu_name] = price

                        booth = Booth.objects.create(
                            name=name,
                            menu=menu_dict,
                            description=description,
                            start_at=start_at,
                            end_at=end_at,
                            location=location,
                            type='푸드트럭'
                        )
                        booth.save() 
                        print(f"{name} 푸드트럭 생성 완료")       

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