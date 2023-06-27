from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font

def save_to_xlsx(data, base_name, file_path):
    workbook = Workbook()

    # Create a separate worksheet for each class
    for class_name, class_data in data.items():
        worksheet = workbook.create_sheet(title=class_name)
        worksheet.append(["Type", "Title", "URL", "Domain", "Byline Date", "Description", "Sitelinks", "Rich Attributes", "Brand Display"])

        if class_name == "websites":
            for website in class_data:
                sitelinks = website.sitelinks if website.sitelinks else {}
                rich_attributes = website.rich_attributes if website.rich_attributes else {}

                # Append the main website row
                worksheet.append(["Website", website.title, website.url, website.domain, website.byline_date, website.description, "", "", website.brand_display])

                # Append each sitelink row
                for i in range(max(len(sitelinks.get("questions", [])), len(sitelinks.get("answers", [])), len(sitelinks.get("dates", [])))):
                    question = sitelinks.get("questions", [""])[i] if sitelinks.get("questions") else ""
                    answer = sitelinks.get("answers", [""])[i] if sitelinks.get("answers") else ""
                    date = sitelinks.get("dates", [""])[i] if sitelinks.get("dates") else ""
                    worksheet.append(["", "", "", "", "", "", question, answer, ""])

                # Append each rich attribute row
                for attribute, value in rich_attributes.items():
                    worksheet.append(["", "", "", "", "", "", "", attribute, value])

    # Remove the default sheet created and save the workbook
    workbook.remove(workbook["Sheet"])
    workbook.save(file_path)