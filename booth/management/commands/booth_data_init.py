from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from booth.models import Booth, MenuImage, LogoImage
import openpyxl, os, json, re
from PIL import Image
from django.core.files import File
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        excel_file = "C:/Users/USER/Desktop/NigthBooth.xlsx"
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb['Sheet1']

        logo_images = "C:/Users/USER/Desktop/image"
        image_list = os.listdir(logo_images)
        for i in range(2,58):
            row = sheet[i]
            operator=row[0].value
            start_end_dates=row[1].value
            location=row[2].value
            section=row[3].value
            name=row[4].value
            concept=row[5].value
            description=row[6].value
            start_at, end_at = self.parse_start_end_dates(start_end_dates)
            error=False
            
            if not self.location_in_choices(location):
                error = True
                print(f"{location} 입력 오류")

            if not error:
                try:
                    booth=Booth.objects.get(operator=operator)
                    booth.start_at=start_at
                    booth.end_at=end_at
                    booth.location=location
                    booth.section=section
                    booth.name=name
                    booth.concept=concept
                    booth.description=description
                    booth.save()
                    print(f"{operator} 수정 완료")
                except Booth.DoesNotExist:
                    booth = Booth.objects.create(
                        operator=operator,
                        start_at=start_at,
                        end_at=end_at,
                        location=location,
                        section=section,
                        name=name,
                        concept=concept,
                        description=description,
                        type='야간부스'
                    )
                    booth.save()
                    print(f"{operator} 생성 완료")

            operator_without_space = operator.replace(" ","")
            menu_index = 1        
            image_path = "C:/Users/USER/Desktop/image"
            logo_index = 1
            while True:
                imagename = f"{operator_without_space}_메뉴판_0{menu_index}"
                filename = f"{image_path}/{imagename}"
                menu_image = self.get_image(filename)
                if not menu_image:
                    if menu_index ==1:
                        print(f"{operator} 문제 있음")
                    print(f"no image name {operator_without_space}_메뉴판_0{menu_index}")
                    break
                ii = File(open(menu_image,"rb"), name=f"{operator}.{menu_image.split('.')[-1]}")
                mi = MenuImage.objects.create(booth_id=booth.id)
                mi.image = ii
                mi.save()
                if (value:= menu_image.split("/")[-1]) in image_list:
                    image_list.remove(value)
                    print("delete complete")
                menu_index +=1

            while True:
                imagename = f"{operator_without_space}_포스터_0{logo_index}"
                filename = f"{image_path}/{imagename}"
                menu_image = self.get_image(filename)
                print(menu_image)
                if not menu_image:
                    if logo_index ==1:
                        print(f"{operator} 문제 있음")
                    print(f"no image name {operator_without_space}_포스터_0{logo_index}")
                    break
                ii = File(open(menu_image,"rb"), name=f"{operator}.{menu_image.split('.')[-1]}")
                mi = LogoImage.objects.create(booth_id=booth.id)
                mi.image = ii
                mi.save()
                if (value:= menu_image.split("/")[-1]) in image_list:
                    image_list.remove(value)
                    print("delete complete")
                logo_index +=1

        print(image_list)

        # 푸드트럭 정보
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
    
    def get_image(self, filepath):
        try:
            jpg = Image.open(filepath+".jpg")
            jpg.close()
            return filepath+".jpg"
        except Exception:
            pass
        try:
            jpeg = Image.open(filepath+".jpeg")
            jpeg.close()
            return filepath+".jpeg"
        except Exception:
            pass
        try:
            png = Image.open(filepath+".png")
            png.close()
            return filepath+".png"
        except Exception:
            pass
        return None