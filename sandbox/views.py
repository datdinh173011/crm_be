from io import BytesIO

import pandas as pd
import xlsxwriter
from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ImportSerializer


class ImportAPIView(APIView):
    serializer_class = ImportSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response(
                    {"status": False, "message": "Provide a valid file"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            excel_file = data.get("file")
            df = pd.read_excel(excel_file, engine="openpyxl")
            profiles = []
            for index, row in df.iterrows():
                first_name = row["FirstName"]
                last_name = row["LastName"]
                email = row["Email"]
                profile = Profile.objects.filter(email=email)
                if profile.exists():
                    continue
                else:
                    profile = Profile(
                        first_name=first_name, last_name=last_name, email=email
                    )
                    profiles.append(profile)
            Profile.objects.bulk_create(profiles)
            return Response(
                {"status": True, "message": "Profile imported successfully!"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": "We could not complete the import process",
                    "error": e,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ExportAPIView(APIView):
    def get(self, request):
        try:
            profiles = Profile.objects.all()
            df = pd.DataFrame.from_records(profiles.values(), exclude=["date_created"])
            excel_file = BytesIO()

            # Create an Excel workbook using xlsxwriter
            workbook = xlsxwriter.Workbook(excel_file, {"in_memory": True})

            # Write the DataFrame to the workbook
            worksheet = workbook.add_worksheet()
            for i, col in enumerate(df.columns):
                worksheet.write(0, i, col)
                for j, value in enumerate(df[col]):
                    worksheet.write(j + 1, i, value)

            # Close the workbook
            workbook.close()

            # Set the BytesIO object's file pointer to the beginning
            excel_file.seek(0)

            # Create an HTTP response with the file content
            response = HttpResponse(
                excel_file.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=ProfilesExport.xlsx"
            return response

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "error": e,
                    "message": "We could not complete the import process",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
