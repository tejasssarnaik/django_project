
from django.shortcuts import render, redirect
import os
import json
import csv
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseServerError
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from Geneapp.models import Workflow
from .models import UserProfile
from .forms import RegistrationForm
import posixpath
import subprocess
from .models import Workflow, UserProfile, UserHistory, IDCounter
from django.utils import timezone
# from.forms import MyForm

# Create your views here.

@login_required(login_url='login')

def index_view(request):
    return render(request, 'Geneapp/index.html')




# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('/index/')
#             else:
#                 messages.error(request, "Your account is not active. Please activate your account.")
#         else:
#             messages.error(request, "Invalid email or password. Please try again.")

#     return render(request, 'Geneapp/login.html')





# def register_view(request):
#     if request.method == 'POST':
#         registration_form = RegistrationForm(request.POST)

#         if registration_form.is_valid():
#             full_name = registration_form.cleaned_data['full_name']
#             email = registration_form.cleaned_data['email']
#             username = registration_form.cleaned_data['username']
#             institute_name = registration_form.cleaned_data['institute_name']
#             designation = registration_form.cleaned_data['designation']
#             password1 = registration_form.cleaned_data['password1']
#             password2 = registration_form.cleaned_data['password2']

#             if password1 != password2:
#                 messages.add_message(request, messages.ERROR, "Passwords do not match.")
#                 return render(request, 'Geneapp/login.html')

#             try:
#                 user = User.objects.get(username=email)
#                 messages.add_message(request, messages.ERROR, "User with this email already exists.")
#                 return render(request, 'Geneapp/login.html')
#             except User.DoesNotExist:
#                 pass

#             try:
#                 user = User.objects.create_user(username=email, email=email, password=password1)
#                 user.first_name = full_name
#                 user.save()

#                 # Create a user profile and save additional information
#                 user_profile = UserProfile(user=user, full_name=full_name, email=email, username=username, institute_name=institute_name, designation=designation)
#                 user_profile.save()

#                 # Send a verification email
#                 current_site = get_current_site(request)
#                 mail_subject = 'Activate your account'
#                 message = render_to_string('Geneapp/verification_email.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(str(user.pk).encode()),
#                     'token': default_token_generator.make_token(user),
#                 })

#                 send_mail(mail_subject, message, 'your_email@example.com', [email])

#                 # Additional registration logic

#                 messages.add_message(request, messages.SUCCESS, "User registered successfully. Please check your email for verification instructions.")
#                 return redirect('/register/')
#             except Exception as e:
#                 messages.add_message(request, messages.ERROR, f"Error: {e}")

#     else:
#         registration_form = RegistrationForm()

#     return render(request, 'Geneapp/login.html', {'registration_form': registration_form})




# def activate_account(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)

#         if default_token_generator.check_token(user, token):
#             if not user.is_active:
#                 user.is_active = True
#                 user.save()
#             messages.success(request, "Your account has been activated! You can now login.")
#         else:
#             messages.error(request, "Invalid activation link.")
#     except Exception as e:
#         messages.error(request, f"Error: {e}")

#     return redirect('login')


from django.utils.encoding import force_bytes,force_str

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/index/')
            else:
                messages.error(request, "Your account is not active. Please activate your account.")
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'Geneapp/login.html')

def register_view(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            full_name = registration_form.cleaned_data['full_name']
            email = registration_form.cleaned_data['email']
            username = registration_form.cleaned_data['username']
            institute_name = registration_form.cleaned_data['institute_name']
            designation = registration_form.cleaned_data['designation']
            password1 = registration_form.cleaned_data['password1']
            password2 = registration_form.cleaned_data['password2']

            if password1 != password2:
                messages.add_message(request, messages.ERROR, "Passwords do not match.")
                return render(request, 'Geneapp/login.html')

            try:
                user = User.objects.get(username=email)
                messages.add_message(request, messages.ERROR, "User with this email already exists.")
                return render(request, 'Geneapp/login.html')
            except User.DoesNotExist:
                pass

            try:
                user = User.objects.create_user(username=email, email=email, password=password1)
                user.first_name = full_name
                user.is_active = False  # User is not active until email verification
                user.save()

                # Create a user profile and save additional information
                user_profile = UserProfile(user=user, full_name=full_name, email=email, username=username, institute_name=institute_name, designation=designation)
                user_profile.save()

               # Send a verification email
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('Geneapp/verification_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })


                send_mail(mail_subject, message, 'your_email@example.com', [email])

                messages.add_message(request, messages.SUCCESS, "User registered successfully. Please check your email for verification instructions.")
                return redirect('/login/')
            except Exception as e:
                messages.add_message(request, messages.ERROR, f"Error: {e}")

    else:
        registration_form = RegistrationForm()

    return render(request, 'Geneapp/login.html', {'registration_form': registration_form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not user.is_active and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid activation link.")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect('login')




def forgot_view(request):
    return render(request, 'Geneapp/forgot-password.html')




def wes_view(request):
    return render(request, 'Geneapp/wes.html')




def wgs_view(request):
    return render(request, 'Geneapp/wgs.html')




def tngs_view(request):
    return render(request, 'Geneapp/tngs.html')




def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            reset_link = f"http://127.0.0.1:8000/reset_password/{uid}/{token}/"  # Replace with your actual URL

            # Send reset link to user's email
            subject = 'Password Reset'
            message = f'''
            Thanks for your interest in GeneAssure - GeneAssure is a cutting-edge solution revolutionizing large-scale genomic data analysis.  

            We just need to verify your email address with link to reset the password to start using GeneAssure.

            Click the link to reset your password: {reset_link}

            If you have problems,

            For any issue, contact us at contact@genespectrum.in.

            Best Regards,
            GeneSpectrum Life Sciences LLP
            '''
            sender = 'admin@example.com'  # Replace with your actual sender email
            recipient_list = [email]
            send_mail(subject, message, sender, recipient_list)

            # Add a success message (optional)
            messages.success(request, "Password reset link sent successfully.")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")

        return redirect('/reset_password/')

    return render(request, 'Geneapp/forgot-password.html')




def reset_password_link(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')

                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Keep the user logged in
                    messages.success(request, "Password updated successfully.")
                    return redirect('login')
                else:
                    messages.error(request, "Passwords do not match.")

            return render(request, 'Geneapp/reset-password.html', {'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, "Invalid reset link.")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect('login')




def wesdata_view(request):
    if request.method == 'POST' and all(request.FILES.get(f) for f in ['fastq1', 'fastq2']):
        fastq1_files = request.FILES.getlist('fastq1')
        fastq2_files = request.FILES.getlist('fastq2')
        bed_files = request.FILES.getlist('bed')
        selected_option = request.POST.get('selected_option')
        new_selected_option = request.POST.get('new_selected_option')
        wes_workflowname = request.POST.get('workflowname')

        selected_option_string = f"{selected_option}"

        # default_fastq1_path = "s3://geneassure-nf-test-data/GA_TEST_DATA/SRR19544453_1.fastq.gz"
        # default_fastq2_path = "s3://geneassure-nf-test-data/GA_TEST_DATA/SRR19544453_2.fastq.gz"
        # fastq_data = [{'SAMPLEID': f'{wes_workflowname}', 'FASTQ1': default_fastq1_path, 'FASTQ2': default_fastq2_path} for _ in range(len(fastq1_files))]

        fastq_pairs = list(zip(fastq1_files, fastq2_files))
        fastq_data = [{'SAMPLEID': f1.name.split('_')[0], 'FASTQ1': f1.name, 'FASTQ2': f2.name} for f1, f2 in fastq_pairs]

        for row in fastq_data:
            row['FASTQ1'] = posixpath.abspath(f'{row["FASTQ1"]}').replace(os.sep, '/')
            row['FASTQ2'] = posixpath.abspath(f'{row["FASTQ2"]}').replace(os.sep, '/')

        csv_path = 'GeneAssure/metadata.csv'
        absolute_csv_path = os.path.abspath(csv_path).replace(os.sep, '/')

        with open(csv_path, mode='w', newline='') as csv_file:
            fieldnames = ['SAMPLEID', 'FASTQ1', 'FASTQ2']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in fastq_data:
                writer.writerow(row)

        bed_files = [posixpath.abspath(f'{file.name}').replace(os.sep, '/') for file in bed_files]

        fasta_path = None  # Default value

        if selected_option == 'Hg38':
            fasta_path = "s3://geneassure-nf-test-data/GA_TEST_DATA/chr1.fasta"


        bed_path = bed_files[0].replace(os.sep, '/') if bed_files else ""
        id_counter, created = IDCounter.objects.get_or_create(pk=1)
        project_id = id_counter.increment_project_id()
        wes_workflow_id = id_counter.increment_workflow_id()

        data = {
            "workflow_id":wes_workflow_id,
            "workflow_name":wes_workflowname,
            "csv": "./"+ csv_path,
            "clinvar":"s3://geneassure-nf-test-data/GA_TEST_DATA/clinvar.vcf.gz",
            "fasta": "s3://geneassure-nf-test-data/GA_TEST_DATA/chr1.fasta",
            "indel": "s3://geneassure-nf-test-data/GA_TEST_DATA/rn_All.chr1.indels.GRCh38.vcf.gz",
            "intervalList": "s3://geneassure-nf-test-data/GA_TEST_DATA/intervalslist.bed",
            "ipdir": "s3://geneassure-nf-test-data/GA_TEST_DATA/",
            "max_cpus": 6,
            "max_memory": "16.GB",
            "max_time": "30.m",
            "output_dir": "s3://geneassure-nf-test-data/GA_TEST_DATA/",
            "paired" : True,
            "processid": "GENEASSURE-TEST",
            "rglb": "lib1",
            "rgpl": "ILLUMINA",
            "rgpu": "unit1",
            "rgsm": "",
            "snp": "s3://geneassure-nf-test-data/GA_TEST_DATA/rn_All.chr1.snvindels.GRCh38.vcf.gz",
            "trim" : "true",
            "bed" : "s3://geneassure-nf-test-data/GA_TEST_DATA/intervalslist.bed",
            "skip_steps" : "",
            "skip_tools" : "deepvariant"
        }

        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)


        wes_samples = (len(fastq1_files) + len(fastq2_files)) // 2
        wes_creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        wes_status = "Running"
        wes_configuration = new_selected_option
        # wes_workflow_id = str(random.randint(1, 99))

        

        context = {
            'wes_configuration': wes_configuration,
            'wes_samples': wes_samples,
            'wes_workflowname':wes_workflowname,
            'wes_creation': wes_creation,
            'wes_status': wes_status,
            'wes_workflow_id': wes_workflow_id,
        }

        user_profile = UserProfile.objects.get(user=request.user)
        history_entry = UserHistory(
            user=user_profile,
            project_id=wes_workflow_id,
            workflow_id=wes_workflow_id,
            task_performance_time=timezone.now(),
            workflow_submission_time=timezone.now(),
            workflow_type=wes_configuration,
            workflow_name=wes_workflowname,
            samples=wes_samples,
            status=wes_status,
        )
        history_entry.save()

        obj = Workflow(Configuration=wes_configuration,Workflow_name=wes_workflowname, Samples=wes_samples, Creation=wes_creation, Status=wes_status, Workflow_ID=wes_workflow_id)
        obj.save()

        history_entry.sample_id = row['SAMPLEID']
        history_entry.save()

        obj.sample_id = row['SAMPLEID']
        obj.save()

        # script_path = 'geneassure.py'  # Change this to the actual path of your script
        # subprocess.Popen(['python', script_path]) 

        return render(request, 'Geneapp/workflow.html', context)
    else:
        return render(request, 'Geneapp/workflow.html')
    



def tngsdata_view(request):
    if request.method == 'POST' and all(request.FILES.get(f) for f in ['fastq1', 'fastq2']):
        fastq1_files = request.FILES.getlist('fastq1')
        fastq2_files = request.FILES.getlist('fastq2')
        bed_files = request.FILES.getlist('bed')
        selected_option = request.POST.get('selected_option')
        new_selected_option = request.POST.get('new_selected_option')
        tngs_workflowname = request.POST.get('workflowname')


        selected_option_string = f"{selected_option}"

        # default_fastq1_path = "s3://geneassure-nf-test-data/GA_TEST_DATA/SRR19544453_1.fastq.gz"
        # default_fastq2_path = "s3://geneassure-nf-test-data/GA_TEST_DATA/SRR19544453_2.fastq.gz"
        # fastq_data = [{'SAMPLEID': f'{tngs_workflowname}', 'FASTQ1': default_fastq1_path, 'FASTQ2': default_fastq2_path} for _ in range(len(fastq1_files))]

        fastq_pairs = list(zip(fastq1_files, fastq2_files))
        fastq_data = [{'SAMPLEID': f1.name.split('_')[0], 'FASTQ1': f1.name, 'FASTQ2': f2.name} for f1, f2 in fastq_pairs]

        for row in fastq_data:
            row['FASTQ1'] = posixpath.abspath(f'{row["FASTQ1"]}').replace(os.sep, '/')
            row['FASTQ2'] = posixpath.abspath(f'{row["FASTQ2"]}').replace(os.sep, '/')

        csv_path = 'GeneAssure/metadata.csv'
        # absolute_csv_path = os.path.abspath(csv_path).replace(os.sep, '/')

        with open(csv_path, mode='w', newline='') as csv_file:
            fieldnames = ['SAMPLEID', 'FASTQ1', 'FASTQ2']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in fastq_data:
                writer.writerow(row)

        bed_files = [posixpath.abspath(f'{file.name}').replace(os.sep, '/') for file in bed_files]

        fasta_path = None  # Default value

        if selected_option == 'Hg38':
            fasta_path = "s3://geneassure-nf-test-data/GA_TEST_DATA/chr1.fasta"

        bed_path = bed_files[0].replace(os.sep, '/') if bed_files else ""

        # Retrieve or create an IDCounter instance
        id_counter, created = IDCounter.objects.get_or_create(pk=1)

        # Get the next project and workflow IDs
        project_id = id_counter.increment_project_id()
        tngs_workflow_id = id_counter.increment_workflow_id()


        data = {
            "workflow_id":tngs_workflow_id,
            "workflow_name":tngs_workflowname,
            "csv": "./"+ csv_path,
            "clinvar":"s3://geneassure-nf-test-data/GA_TEST_DATA/clinvar.vcf.gz",
            "fasta": "s3://geneassure-nf-test-data/GA_TEST_DATA/chr1.fasta",
            "indel": "s3://geneassure-nf-test-data/GA_TEST_DATA/rn_All.chr1.indels.GRCh38.vcf.gz",
            "intervalList": "s3://geneassure-nf-test-data/GA_TEST_DATA/intervalslist.bed",
            "ipdir": "s3://geneassure-nf-test-data/GA_TEST_DATA/",
            "max_cpus": 6,
            "max_memory": "16.GB",
            "max_time": "30.m",
            "output_dir": "s3://geneassure-nf-test-data/GA_TEST_DATA/",
            "paired" : True,
            "processid": "GENEASSURE-TEST",
            "rglb": "lib1",
            "rgpl": "ILLUMINA",
            "rgpu": "unit1",
            "rgsm": "",
            "snp": "s3://geneassure-nf-test-data/GA_TEST_DATA/rn_All.chr1.snvindels.GRCh38.vcf.gz",
            "trim" : "true",
            "bed" : "s3://geneassure-nf-test-data/GA_TEST_DATA/intervalslist.bed",
            "skip_steps" : "",
            "skip_tools" : "deepvariant"
        }

        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)


        tngs_samples = (len(fastq1_files) + len(fastq2_files)) // 2
        tngs_creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tngs_status = "Running"
        tngs_configuration = new_selected_option
        # tngs_workflow_id = str(random.randint(1, 99))

      
        context = {
            'tngs_configuration': tngs_configuration,
            'tngs_samples': tngs_samples,
            'tngs_workflowname':tngs_workflowname,
            'tngs_creation': tngs_creation,
            'tngs_status': tngs_status,
            'tngs_workflow_id': tngs_workflow_id,
        }

        user_profile = UserProfile.objects.get(user=request.user)
        history_entry = UserHistory(
            user=user_profile,
            project_id=tngs_workflow_id,
            workflow_id=tngs_workflow_id,
            task_performance_time=timezone.now(),
            workflow_submission_time=timezone.now(),
            workflow_type=tngs_configuration,
            workflow_name=tngs_workflowname,
            samples=tngs_samples,
            status=tngs_status,
        )
        history_entry.save()

        obj = Workflow(Configuration=tngs_configuration, Samples=tngs_samples, Workflow_name=tngs_workflowname, Creation=tngs_creation, Status=tngs_status, Workflow_ID=tngs_workflow_id)
        obj.save()


        history_entry.sample_id = row['SAMPLEID']
        history_entry.save()

        obj.sample_id = row['SAMPLEID']
        obj.save()

        # script_path = 'geneassure.py'  # Change this to the actual path of your script
        # subprocess.Popen(['python', script_path]) 

        return render(request, 'Geneapp/workflow.html', context)
    else:
        return render(request, 'Geneapp/workflow.html')




# def wgsdata_view(request):
#     if request.method == 'POST':
#         selected_project_id = request.session.get('selected_project_id')
#         selected_project_name = request.session.get('selected_project_name')
#         workflow_name = request.POST.get('workflowname')
#         workflow_type = request.POST.get('selected_option')
#         fastq_option = request.POST.get('selected_fastq_option')
#         reference_genome = request.POST.get('reference_genome')
#         sample_name = request.POST.get('samplename')

#         # Split the fastq_option string into separate filenames
#         fastq_files = fastq_option.split(',')

#         # Ensure that there are two files
#         if len(fastq_files) != 2:
#             # Handle the case where there are not exactly two filenames
#             # You can raise an error, redirect, or handle it as needed
#             pass

#         # Assign the filenames to separate variables
#         fastq_file1 = fastq_files[0].strip()  # Remove any leading/trailing spaces
#         fastq_file2 = fastq_files[1].strip()  # Remove any leading/trailing spaces

        # # Print the individual filenames
        # print(f"First Fastq File: {fastq_file1}")
        # print(f"Second Fastq File: {fastq_file2}")

        # # Sample data for CSV
        # pname=selected_project_name
        # pid = (selected_project_name) +'_'+ str(selected_project_id)
        # wid = 1
        # sample_id = sample_name
        # fastq1 = fastq_file1 # Get selected Fastq1 file path
        # fastq2 = fastq_file2 # You will replace this with the actual path

        # # CSV data to write
        # csv_data = [
        #     ['PID', 'WID', 'SAMPLEID', 'FASTQ1', 'FASTQ2'],
        #     [pid, wid, sample_id, fastq1, fastq2],
        # ]

        # # File path for the CSV file
        # csv_filename = 'GeneAssure/sample.csv'
        # csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)

        # # Writing CSV data to file
        # with open(csv_path, mode='w', newline='') as csv_file:
        #     writer = csv.writer(csv_file)
        #     writer.writerows(csv_data)

#         # Returning a success message or HTTP response
#         return HttpResponse("CSV file generated successfully!")
#     else:
#         return HttpResponse("Only POST requests are allowed!")
    
from django.urls import reverse
from .models import IDCounter, UserProfile, UserHistory, Workflow, Project

def wgsdata_view(request):
    if request.method == 'POST':
        selected_project_id = request.session.get('selected_project_id')
        selected_project_name = request.session.get('selected_project_name')
        workflow_name = request.POST.get('workflowname')
        workflow_type = request.POST.get('selected_option')
        fastq_option = request.POST.get('selected_fastq_option')
        reference_genome = request.POST.get('reference_genome')
        sample_name = request.POST.get('samplename')

        # Split the fastq_option string into separate filenames
        fastq_files = fastq_option.split(',')

        # Ensure that there are two files
        if len(fastq_files) != 2:
            # Handle the case where there are not exactly two filenames
            # You can raise an error, redirect, or handle it as needed
            pass

        # Assign the filenames to separate variables
        fastq_file1 = fastq_files[0].strip()  # Remove any leading/trailing spaces
        fastq_file2 = fastq_files[1].strip()  # Remove any leading/trailing spaces
        
        # Print the individual filenames
        print(f"First Fastq File: {fastq_file1}")
        print(f"Second Fastq File: {fastq_file2}")

        # Sample data for CSV
        pname=selected_project_name
        pid = (selected_project_name) +'_'+ str(selected_project_id)
        wid = 1
        sample_id = sample_name
        fastq1 = fastq_file1 # Get selected Fastq1 file path
        fastq2 = fastq_file2 # You will replace this with the actual path

        # CSV data to write
        csv_data = [
            ['PID', 'WID', 'SAMPLEID', 'FASTQ1', 'FASTQ2'],
            [pid, wid, sample_id, fastq1, fastq2],
        ]

        # File path for the CSV file
        csv_filename = 'GeneAssure/sample.csv'
        csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)

        # Writing CSV data to file
        with open(csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)

        # Sample data for CSV
        project = Project.objects.get(id=selected_project_id)  # Fetch the selected project
        samples = (len(fastq_files)) // 2
        creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Running"

        id_counter, created = IDCounter.objects.get_or_create(pk=1)

        workflow_id = id_counter.increment_workflow_id()

        user_profile = UserProfile.objects.get(user=request.user)
        history_entry = UserHistory(
            user=user_profile,
            project=project,  # Link the UserHistory entry to the selected project
            workflow_id=workflow_id,
            task_performance_time=datetime.now(),
            workflow_submission_time=datetime.now(),
            workflow_type=workflow_type,
            workflow_name=workflow_name,
            reference_genome = reference_genome,
            samples=samples,
            sample_id=sample_name,
            status=status,
        )
        history_entry.save()

        obj = Workflow(
            Configuration=workflow_type,
            Workflow_name=workflow_name,
            Samples=samples,
            Creation=creation,
            Status=status,
            Workflow_ID=workflow_id,
            reference_genome = reference_genome,
            sample_id=sample_name
        )
        obj.save()

        return redirect(reverse('workflow_details', kwargs={'Workflow_ID': workflow_id}))
    else:
        return HttpResponse("Only POST requests are allowed!")




    # if request.method == 'POST' and all(request.FILES.get(f) for f in ['fastq1', 'fastq2']):
    #     fastq1_files = request.FILES.getlist('fastq1')
    #     fastq2_files = request.FILES.getlist('fastq2')
    #     selected_option = request.POST.get('selected_option')
    #     new_selected_option = request.POST.get('new_selected_option')
    #     workflowname = request.POST.get('workflowname')

    #     fastq_pairs = list(zip(fastq1_files, fastq2_files))
    #     fastq_data = [{'SAMPLEID': f1.name.split('_')[0], 'FASTQ1': f1.name, 'FASTQ2': f2.name} for f1, f2 in fastq_pairs]

    #     # Create metadata CSV file
    #     csv_filename = 'GeneAssure/metadata.csv'
    #     csv_path = os.path.join(settings.MEDIA_ROOT, csv_filename)

    #     with open(csv_path, mode='w', newline='') as csv_file:
    #         fieldnames = ['SAMPLEID', 'FASTQ1', 'FASTQ2']
    #         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         for row in fastq_data:
    #             writer.writerow(row)

    #     # Create data JSON file
    #     data = {
    #         'workflow_id': '',
    #         'workflow_name': workflowname,
    #         'csv': csv_filename,
    #         'clinvar': "s3://geneassure-nf-test-data/GA_TEST_DATA/clinvar.vcf.gz",
    #         'fasta': "s3://geneassure-nf-test-data/GA_TEST_DATA/chr1.fasta",
    #         'indel': "s3://geneassure-nf-test-data/GA_TEST_DATA/rn_All.chr1.indels.GRCh38.vcf.gz",
    #         'intervalList': "s3://geneassure-nf-test-data/GA_TEST_DATA/intervalslist.bed",
    #         'ipdir': "s3://geneassure-nf-test-data/GA_TEST_DATA/",
    #         'max_cpus': 4,
    #         'max_memory': "8.GB",
    #         'max_time': "30.m",
    #         'output_dir': "s3://geneassure-nf-test-data/GA_TEST_DATA/",
    #         'paired': True,
    #         'processid': "GENEASSURE-TEST",
    #         'rglb': "lib1",
    #         'rgpl': "ILLUMINA",
    #         'rgpu': "unit1",
    #         'rgsm': "",
    #         'snp': "s3://geneassure-nf-test-data/GA_TEST_DATA/rn_All.chr1.snvindels.GRCh38.vcf.gz",
    #         'trim': "true",
    #         'bed': "s3://geneassure-nf-test-data/GA_TEST_DATA/intervalslist.bed",
    #         'skip_steps': "",
    #         'skip_tools': "deepvariant"
    #     }

    #     json_filename = 'GeneAssure/data.json'
    #     json_path = os.path.join(settings.MEDIA_ROOT, json_filename)

    #     with open(json_path, 'w') as json_file:
    #         json.dump(data, json_file)

    #     # Additional logic
    #     samples = (len(fastq1_files) + len(fastq2_files)) // 2
    #     creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     status = "Running"

    #     # Retrieve or create an IDCounter instance
    #     id_counter, created = IDCounter.objects.get_or_create(pk=1)

    #     # Get the next project and workflow IDs
    #     project_id = id_counter.increment_project_id()
    #     workflow_id = id_counter.increment_workflow_id()

    #     context = {
    #         'samples': samples,
    #         'workflowname': workflowname,
    #         'creation': creation,
    #         'status': status,
    #         'workflow_id': workflow_id,
    #         'configuration': new_selected_option,
    #     }

    #     # Save to database
    #     user_profile = UserProfile.objects.get(user=request.user)
    #     history_entry = UserHistory(
    #         user=user_profile,
    #         project_id=project_id,
    #         workflow_id=workflow_id,
    #         task_performance_time=datetime.now(),
    #         workflow_submission_time=datetime.now(),
    #         workflow_type=new_selected_option,
    #         workflow_name=workflowname,
    #         samples=samples,
    #         sample_id=row['SAMPLEID'],
    #         status=status,
    #     )
    #     history_entry.save()

    #     obj = Workflow(
    #         Configuration=new_selected_option,
    #         Workflow_name=workflowname,
    #         Samples=samples,
    #         Creation=creation,
    #         Status=status,
    #         Workflow_ID=workflow_id,
    #         sample_id=row['SAMPLEID']
    #     )
    #     obj.save()

    #     return render(request, 'Geneapp/workflow.html', context)

    # else:
    #     return render(request, 'Geneapp/workflow.html')



# def user_history(request):
#     history_data = UserHistory.objects.all()
#     return render(request, 'Geneapp/user_history.html', {'history_data':history_data})

@login_required
def user_history(request, project_id=None):
    user_profile = request.user.userprofile
    projects = Project.objects.all()

    selected_project_name = None
    if project_id:
        selected_project = Project.objects.get(id=project_id)
        selected_project_name = selected_project.name
        history_data = UserHistory.objects.filter(user=user_profile, project=selected_project).order_by('-workflow_submission_time')
    else:
        history_data = UserHistory.objects.filter(user=user_profile).order_by('-workflow_submission_time')

    return render(request, 'Geneapp/user_history.html', {'history_data': history_data, 'projects': projects, 'selected_project_name': selected_project_name})








    



def landingpage_view(request):
    return render(request,'Geneapp/landingpage.html')



def analysis_view(request):
    return render(request,'Geneapp/analysis.html')



@login_required(login_url='login')
def profile(request):
    return render(request,'Geneapp/profile.html')



# from django.shortcuts import render, get_object_or_404

# def workflow_details_view(request, Workflow_ID):
#     entry = get_object_or_404(UserHistory, id=Workflow_ID)
#     return render(request, 'Geneapp/workflow_details.html', {'entry': entry})







# import urllib.request
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from .forms import FileLinkForm

# def process_file(file_url):
#     try:
#         # Open the file URL and read its content
#         with urllib.request.urlopen(file_url) as response:
#             file_content = response.read().decode('utf-8')

#         # Split the content into rows and extract the last row
#         rows = file_content.strip().split('\n')
#         last_row = rows[-1]

#         # Split the last row into columns
#         columns = last_row.split('\t')

#         # Extract the "status" column value
#         status_column_value = columns[4]

#         return status_column_value

#     except Exception as e:
#         # Handle errors, such as invalid URL or connection issues
#         return f"Error: {e}"

# def view_file(request, Workflow_ID):
#     entry = get_object_or_404(UserHistory, id=Workflow_ID)

#     if request.method == 'POST':
#         form = FileLinkForm(request.POST)
#         if form.is_valid():
#             file_url = form.cleaned_data['file_link']
#             status_column_value = process_file(file_url)

#             return render(request, 'Geneapp/workflow_details.html', {'form': form, 'status_column_value': status_column_value, 'entry': entry})

#     else:
#         form = FileLinkForm()

#     return render(request, 'Geneapp/workflow_details.html', {'form': form, 'entry': entry})


# def workflow_details_view(request, Workflow_ID):
#     entry = get_object_or_404(UserHistory, id=Workflow_ID)
#     return view_file(request, Workflow_ID)




def custom_404_view(request, exception):
    return render(request, 'Geneapp/404.html', status=404)



# def igv_view(request):
#     return render(request,'Geneapp/igv.html')



# import os
# from django.http import HttpResponse
# from .models import UserHistory
# from django.shortcuts import render, get_object_or_404
# import csv

# def process_csv(file_path):
#     with open(file_path, 'r') as csvfile:
#         csv_reader = csv.DictReader(csvfile, delimiter='\t')
#         for row in csv_reader:
#             yield row

# def workflow_details_view2(request, Workflow_ID):
#     entry = get_object_or_404(UserHistory, id=Workflow_ID)

#     # Check if the file path is submitted via POST
#     if request.method == 'POST':
#         file_path = request.POST.get('file_link', '')

#         # Process the file and save the processed data to the UserHistory model
#         entry.file_content = list(process_csv(file_path))
#         entry.save()

#         # Save the file path in the session for future reference
#         request.session['file_path_' + str(Workflow_ID)] = file_path

#     # If GET request, check if there is previously saved data for this workflow
#     elif 'file_path_' + str(Workflow_ID) in request.session:
#         file_path = request.session['file_path_' + str(Workflow_ID)]

#         # Check if the file path is valid
#         if os.path.exists(file_path):
#             entry.file_content = list(process_csv(file_path))
#             entry.save()
#         else:
#             # Handle the case where the file no longer exists
#             return HttpResponse("File not found")

#     # Display the template with the processed data for the particular Workflow_ID
#     if entry.file_content:
#         return render(request, 'Geneapp/workflow_details2.html', {'entry': entry, 'rows_data': entry.file_content})

#    # Handle GET requests or other cases
#     return render(request, 'Geneapp/workflow_details2.html', {'entry': entry})





# import os
# import csv
# from django.http import HttpResponse
# from django.shortcuts import render, get_object_or_404
# from .models import UserHistory

# def process_csv(file_path):
#     with open(file_path, 'r') as csvfile:
#         csv_reader = csv.DictReader(csvfile, delimiter='\t')
#         for row in csv_reader:
#             yield row

# def workflow_details_view2(request, Workflow_ID):
#     entry = get_object_or_404(UserHistory, id=Workflow_ID)

#     # Define the igv_options dictionary
#     igv_options = {
#         'genome': 'hg38',
#         'locus': 'chr8:127,736,588-127,739,371',
#         'tracks': [
#             {
#                 'name': "Color by attribute biotype",
#                 'type': "annotation",
#                 'format': "gff3",
#                 'displayMode': "expanded",
#                 'height': 300,
#                 # 'url': 'file:///C:/Users/Tejas/Desktop/csv_mysql/New_folder_3/DjangoGeneAssure_26_12/trim_SRR7002370_1.fastq_1_fltr_1_final_1_hpc_norm_vf.vcf.gz',
#                 # 'indexURL': 'file:///C:/Users/Tejas/Desktop/csv_mysql/New_folder_3/DjangoGeneAssure_26_12/trim_SRR7002370_1.fastq_1_fltr_1_final_1_hpc_norm_vf.vcf.gz.tbi',
#                 'url': "https://s3.amazonaws.com/igv.org.genomes/hg38/Homo_sapiens.GRCh38.94.chr.gff3.gz",
#                 'indexURL': "https://s3.amazonaws.com/igv.org.genomes/hg38/Homo_sapiens.GRCh38.94.chr.gff3.gz.tbi",
#                 'visibilityWindow': 1000000,
#                 'colorBy': "biotype",
#                 'colorTable': 
#                     {
#                         "antisense": "blueviolet",
#                         "protein_coding": "blue",
#                         "retained_intron": "rgb(0, 150, 150)",
#                         "processed_transcript": "purple",
#                         "processed_pseudogene": "#7fff00",
#                         "unprocessed_pseudogene": "#d2691e",
#                         "*": "black"
#                     }
                
#             }
#         ]
#     }

#     # Check if the file path is submitted via POST
#     if request.method == 'POST':
#         file_path = request.POST.get('file_link', '')

#         # Process the file and save the processed data to the UserHistory model
#         entry.file_content = list(process_csv(file_path))
#         entry.save()

#         # Save the file path in the session for future reference
#         request.session['file_path_' + str(Workflow_ID)] = file_path

#     # If GET request, check if there is previously saved data for this workflow
#     elif 'file_path_' + str(Workflow_ID) in request.session:
#         file_path = request.session['file_path_' + str(Workflow_ID)]

#         # Check if the file path is valid
#         if os.path.exists(file_path):
#             entry.file_content = list(process_csv(file_path))
#             entry.save()
#         else:
#             # Handle the case where the file no longer exists
#             return HttpResponse("File not found")

#     # Display the template with the processed data for the particular Workflow_ID
#     if entry.file_content:
#         return render(request, 'Geneapp/workflow_details2.html', {'entry': entry, 'rows_data': entry.file_content, 'igv_options': igv_options})

#     # Handle GET requests or other cases
#     return render(request, 'Geneapp/workflow_details2.html', {'entry': entry, 'igv_options': igv_options})






from django.conf import settings
from django.core.files.storage import FileSystemStorage

def convert_bytes(size, unit=None):
    # Convert bytes to other units
    units = ['bytes', 'KB', 'MB', 'GB', 'TB']
    if unit and unit in units:
        idx = units.index(unit)
    else:
        idx = 0
        while size >= 1024 and idx < len(units)-1:
            size /= 1024
            idx += 1
    return size, units[idx]

def data_analysis(request):
    if request.method == 'POST' and request.FILES.getlist('file'):
        # Handling file uploads (code omitted for brevity)
        pass
    else:
        fastq_extensions = ['fastq', 'fastq.gz', 'fq', 'fq.gz']
        upload_dir = os.path.join(settings.BASE_DIR, 'upload')

        fastq_files = []
        other_files = []

        # Iterate through files in the upload directory and classify them based on extensions
        for filename in os.listdir(upload_dir):
            if filename.lower().endswith(tuple(fastq_extensions)):
                fastq_files.append({
                    'file_name': filename,
                    'file_type': 'Fastq',
                    'file_size': os.path.getsize(os.path.join(upload_dir, filename)),
                    'uploaded_by': User.objects.get(username=request.user.username).first_name,  # Provide the user who uploaded the file
                    'status': 'Pending',  # Provide the status of the file
                })
            else:
                other_files.append({
                    'file_name': filename,
                    'file_type': 'Other',
                    'file_size': os.path.getsize(os.path.join(upload_dir, filename)),
                    'uploaded_by': User.objects.get(username=request.user.username).first_name, # Provide the user who uploaded the file
                    'status': 'Pending',  # Provide the status of the file
                })

        projects = Project.objects.all()
        return render(request, 'Geneapp/data_analysis.html', {
            'fastq_files': fastq_files,
            'other_files': other_files,
            'projects': projects,
        })

def data_analysis_project(request, project_id):
    fastq_extensions = ['fastq', 'fastq.gz', 'fq', 'fq.gz']
    upload_dir = os.path.join(settings.BASE_DIR, 'upload', str(project_id))

    fastq_files = []
    other_files = []
    trimmed_files = []

    # Fetch Fastq Files (excluding trimmed files)
    for filename in os.listdir(upload_dir):
        if filename.lower().endswith(tuple(fastq_extensions)):
            # Check if the file is not trimmed
            if 'trimmed' not in filename.lower():
                fastq_files.append({
                    'file_name': filename,
                    'file_type': 'Fastq',
                    'file_size': os.path.getsize(os.path.join(upload_dir, filename)),
                    'uploaded_by': User.objects.get(username=request.user.username).first_name,
                    'status': 'Pending',
                    'report_link': f'{filename}_report.html'  # Adjust as needed for your report links
                })
        else:
            other_files.append({
                'file_name': filename,
                'file_type': 'Other',
                'file_size': os.path.getsize(os.path.join(upload_dir, filename)),
                'uploaded_by': User.objects.get(username=request.user.username).first_name,
                'status': 'Pending',
            })

    # Fetch Trimmed Files
    trimmed_dir = os.path.join(upload_dir)
    if os.path.exists(trimmed_dir):
        for filename in os.listdir(trimmed_dir):
            # Check if filename ends with "_trimmed"
            if filename.lower().endswith('_trimmed.fastq.gz'):
                trimmed_files.append({
                    'file_name': filename,
                    'file_type': 'Trimmed',
                    'file_size': os.path.getsize(os.path.join(trimmed_dir, filename)),
                    'uploaded_by': User.objects.get(username=request.user.username).first_name,
                    # 'status': 'Trimmed',
                    # 'file_path': os.path.join(trimmed_dir, filename),  # Include the file path
                })
    
    projects = Project.objects.all()
# Get the selected project's name
    selected_project = get_object_or_404(Project, id=project_id)
    selected_project_name = selected_project.name


    # Pass the selected project's name and ID to the workflow_select view
    request.session['selected_project_name'] = selected_project_name
    request.session['selected_project_id'] = project_id

    # Pass the selected project's name to the template context
    return render(request, 'Geneapp/data_analysis.html', {
        'fastq_files': fastq_files,
        'other_files': other_files,
        'trimmed_files': trimmed_files,
        'projects': projects,
        'selected_project_id': project_id,
        'selected_project_name': selected_project_name,
    })



from .models import Project
def create_project(request):

    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')

        # Generate a random 4-digit project ID
        project_id = random.randint(1000, 9999)

        # Save project to the database
        new_project = Project(id=project_id, name=project_name, description=project_description)
        new_project.save()


        # Create project folder with project ID
        project_folder_path = os.path.join(settings.BASE_DIR, 'upload', str(project_id))
        os.makedirs(project_folder_path)
        return HttpResponse("project created...!!!")

    return render(request, 'Geneapp/data_analysis.html')




def workflow_select(request):
    # Get the selected files from the session
    selected_files = request.session.get('selected_files', [])

    # Separate files for Fastq1, Fastq2, and Trimmed
    fastq1_files = []
    fastq2_files = []
    trimmed1_files = []
    trimmed2_files = []

    for file_path in selected_files:
        file_name = os.path.basename(file_path)
        if file_name.endswith('_1.fastq') or file_name.endswith('_1.fastq.gz'):
            fastq1_files.append({
                'file_path': file_path,
                'file_name': file_name,
            })
        elif file_name.endswith('_2.fastq') or file_name.endswith('_2.fastq.gz'):
            fastq2_files.append({
                'file_path': file_path,
                'file_name': file_name,
            })
        elif file_name.endswith('_1_trimmed.fastq.gz'):
            trimmed1_files.append({
                'file_path': file_path,
                'file_name': file_name,
            })
        elif file_name.endswith('_2_trimmed.fastq.gz'):
            trimmed2_files.append({
                'file_path': file_path,
                'file_name': file_name,
            })

    project_id = request.session.get('selected_project_id')
    upload_dir = os.path.join(settings.BASE_DIR, 'upload', str(project_id))
    other_files = []

    for filename in os.listdir(upload_dir):
        if not filename.lower().endswith(('fastq', 'fastq.gz', 'fq', 'fq.gz')):
            other_files.append({
                'file_name': filename,
                'file_path': os.path.join(upload_dir, filename)
            })

    # Get the list of projects
    projects = Project.objects.all()
            
    # Get the selected project name and ID from the session
    selected_project_name = request.session.get('selected_project_name', '')
    selected_project_id = request.session.get('selected_project_id', '')

    # Pass all files to the template
    return render(request, 'Geneapp/workflowselect.html', {
        'fastq1_files': fastq1_files,
        'fastq2_files': fastq2_files,
        'trimmed1_files': trimmed1_files,
        'trimmed2_files': trimmed2_files,
        'selected_project_name': selected_project_name,
        'selected_project_id': selected_project_id,
        'projects': projects,
        'other_files': other_files,
    })


 
 
from GeneAssure_FASTQC_LNX_main.fastqc import RUN_FASTQC

def run_fastqc(request):
    if request.method == 'POST':
        selected_files = request.POST.getlist('selected_files')  # Get the selected file paths from the form
        selected_project_id = request.POST.get('selected_project_id')  # Get the selected project ID

        csv_data = []
        for file_path in selected_files:
            file_name = os.path.basename(file_path)
            sample_id = file_name.split('_')[0]  # Assuming sample ID is the part before the first underscore
            fastq1_path = file_path
            fastq2_path = file_path  # Assuming FASTQ1 and FASTQ2 paths are the same for single-end data

            # Modify the paths to include the selected project ID
            fastq1_path_formatted = f'E:/djangoProject/DjangoGeneAssure_30_12/upload/{selected_project_id}/{file_name}'
            fastq2_path_formatted = f'E:/djangoProject/DjangoGeneAssure_30_12/upload/{selected_project_id}/{file_name}'

            csv_data.append({
                'PID': selected_project_id,
                'SAMPLEID': sample_id,
                'FASTQ1': fastq1_path_formatted,
                'FASTQ2': fastq2_path_formatted,
            })

        # Write CSV data to a file
        csv_path = 'C:/Users/Tejas/Desktop/csv_mysql/New_folder_3/DjangoGeneAssure_31_12/GeneAssure/fastqc.csv'
        with open(csv_path, mode='w', newline='') as csv_file:
            fieldnames = ['PID', 'SAMPLEID', 'FASTQ1', 'FASTQ2']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)

        # Generate configuration file content
        config_content = f"""\
csvFile="{csv_path}"
outputDir="E:/djangoProject/DjangoGeneAssure_30_12/upload"
threads=16
"""

        # Write configuration file
        config_path = 'fastqc.cfg'
        with open(config_path, 'w') as config_file:
            config_file.write(config_content)

        # RUN_FASTQC("E:\djangoProject\DjangoGeneAssure_30_12\\fastqc.cfg")
        request.session['selected_files'] = selected_files


        return redirect("selectworkflow")

    # If the request method is not POST or if the form wasn't submitted, return to the same page
    return render(request, 'Geneapp/data_analysis.html')






# def data_analysis1(request):
    
#  return render(request,'Geneapp/data_analysis1.html')

from django.http import JsonResponse
def upload_to_project(request):
    if request.method == 'POST' and request.FILES.getlist('file'):
        project_id = request.POST.get('project_id')
        project_folder = os.path.join(settings.BASE_DIR, 'upload', str(project_id))

        if not os.path.exists(project_folder):
            os.makedirs(project_folder)

        for file in request.FILES.getlist('file'):
            file_path = os.path.join(project_folder, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        return JsonResponse({'message': 'Files uploaded successfully to the selected project'})

    else:
        return JsonResponse({'error': 'No files or incorrect method'})
    

def run_trimming(request):
    if request.method == 'POST':
        selected_files = request.POST.getlist('selected_files')  # Get the selected file paths from the form
        selected_project_id = request.POST.get('selected_project_id')  # Get the selected project ID

        csv_data = []
        for file_path in selected_files:
            file_name = os.path.basename(file_path)
            sample_id = file_name.split('_')[0]  # Assuming sample ID is the part before the first underscore
            fastq1_path = file_path
            fastq2_path = file_path  # Assuming FASTQ1 and FASTQ2 paths are the same for single-end data

            # Modify the paths to include the selected project ID
            fastq1_path_formatted = f'E:/djangoProject/DjangoGeneAssure_30_12/upload/{selected_project_id}/{file_name}'
            fastq2_path_formatted = f'E:/djangoProject/DjangoGeneAssure_30_12/upload/{selected_project_id}/{file_name}'

            csv_data.append({
                'PID': selected_project_id,
                'SAMPLEID': sample_id,
                'FASTQ1': fastq1_path_formatted,
                'FASTQ2': fastq2_path_formatted,
            })

        # Write CSV data to a file
        csv_path = 'E:/djangoProject/DjangoGeneAssure_30_12/GeneAssure/trimm.csv'
        with open(csv_path, mode='w', newline='') as csv_file:
            fieldnames = ['PID', 'SAMPLEID', 'FASTQ1', 'FASTQ2']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)

        # Generate configuration file content
        config_content = f"""\
csvFile="{csv_path}"
outputDir="E:/djangoProject/DjangoGeneAssure_30_12/upload"
threads=16
"""

        # Write configuration file
        config_path = 'trimm.cfg'
        with open(config_path, 'w') as config_file:
            config_file.write(config_content)

        # RUN_FASTQC("E:\djangoProject\DjangoGeneAssure_30_12\\fastqc.cfg")
        request.session['selected_files'] = selected_files


        return redirect("selectworkflow")

    # If the request method is not POST or if the form wasn't submitted, return to the same page
    return render(request, 'Geneapp/data_analysis.html')






# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse

# def workflow_details_view(request, Workflow_ID):
#     # Get the UserHistory object
#     entry = get_object_or_404(UserHistory, id=Workflow_ID)
    
#     # Read the log file
#     log_file_path = "C:\\Users\\Tejas\Desktop\\csv_mysql\\New_folder_3\\DjangoGeneAssure_31_12\\GeneAssure_FASTQC_LNX_main\\bin\\project1\\WES\\test_workflow\\LOGS\\test_workflow.trace.log"
#     progress_data = []
#     line_status = {}

#     # Read the content of the log file
#     with open(log_file_path, 'r') as file:
#         log_content = file.readlines()

#         # Append each line to progress_data and determine status
#         for line in log_content:
#             progress_data.append(line.strip())
#             # Determine the status of each line
#             if 'MAPPING START' in line:
#                 line_status['MAPPING'] = 'running'
#             elif 'MAPPING END' in line:
#                 line_status['MAPPING'] = 'completed'
#             elif 'MAPPING ERROR' in line:
#                 line_status['MAPPING'] = 'error'
                
#             if 'BAM-PROCESSING START' in line:
#                 line_status['BAM_PROCESSING'] = 'running'
#             elif 'BAM-PROCESSING END' in line:
#                 line_status['BAM_PROCESSING'] = 'completed'
#             elif 'BAM-PROCESSING ERROR' in line:
#                 line_status['BAM_PROCESSING'] = 'error'
                
#             if 'VCF CALLING START' in line:
#                 line_status['VCF_CALLING'] = 'running'
#             elif 'VCF-FILTERATION	END' in line:
#                 line_status['VCF_CALLING'] = 'completed'
#             elif 'VCF CALLING ERROR' in line:
#                 line_status['VCF_CALLING'] = 'error'
                
#             elif 'VCF-PROCESSING START' in line:
#                 line_status['VCF_PROCESSING'] = 'running'
#             elif 'CONVERT-MERGED-TABLE-TO-VCF	END' in line:
#                 line_status['VCF_PROCESSING'] = 'completed'
#             elif 'VCF-PROCESSING ERROR' in line:
#                 line_status['VCF_PROCESSING'] = 'error'
                
#             elif 'VCF-ANNOTATION START' in line:
#                 line_status['VCF_ANNOTATION'] = 'running'
#             elif 'VCF-ANNOTATION END' in line:
#                 line_status['VCF_ANNOTATION'] = 'completed'
#             elif 'VCF_ANNOTATION ERROR' in line:
#                 line_status['VCF_ANNOTATION'] = 'error'

#     # Render the template with data
#     return render(request, 'Geneapp/workflow_details.html', {'entry': entry, 'progress_data': progress_data, 'line_status': line_status})





# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# import os

# def workflow_details_view(request, Workflow_ID):
#     # Get the UserHistory object
#     entry = get_object_or_404(UserHistory, id=Workflow_ID)
    
#     # Construct the file path dynamically based on the user's project name and workflow name
#     base_path = "C:\\Users\\Tejas\\Desktop\\csv_mysql\\New_folder_3\\DjangoGeneAssure_31_12\\GeneAssure_FASTQC_LNX_main\\bin\\"
#     project_path = entry.project.name.replace(" ", "_")  # Replace spaces with underscores
#     workflow_path = entry.workflow_name.replace(" ", "_")  # Replace spaces with underscores
#     log_directory = os.path.join(base_path, project_path, "WES", workflow_path, "LOGS")
    
#     # List all files in the directory
#     files = os.listdir(log_directory)
    
#     # Filter for files ending with .trace.log and get the last one
#     trace_logs = [file for file in files if file.endswith(".trace.log")]
#     if trace_logs:
#         trace_log_filename = sorted(trace_logs)[-1]  # Get the last one
#         log_file_path = os.path.join(log_directory, trace_log_filename)
#     else:
#         log_file_path = None  # No .trace.log file found

#     progress_data = []
#     line_status = {}

#     # Read the content of the log file
#     with open(log_file_path, 'r') as file:
#         log_content = file.readlines()

       
#         # Append each line to progress_data and determine status
#         for line in log_content:
#             progress_data.append(line.strip())
#             # Determine the status of each line
#             if 'MAPPING	START' in line:
#                 line_status['MAPPING'] = 'running'
#             elif 'MAPPING	END' in line:
#                 line_status['MAPPING'] = 'completed'
#             elif 'MAPPING ERROR' in line:
#                 line_status['MAPPING'] = 'error'
                
#             if 'BAM-PROCESSING	START' in line:
#                 line_status['BAM_PROCESSING'] = 'running'
#             elif 'BAM-PROCESSING	END' in line:
#                 line_status['BAM_PROCESSING'] = 'completed'
#             elif 'BAM-PROCESSING ERROR' in line:
#                 line_status['BAM_PROCESSING'] = 'error'
                
#             if 'VCF CALLING	START' in line:
#                 line_status['VCF_CALLING'] = 'running'
#             elif 'VCF-FILTERATION	END' in line:
#                 line_status['VCF_CALLING'] = 'completed'
#             elif 'VCF CALLING ERROR' in line:
#                 line_status['VCF_CALLING'] = 'error'
                
#             elif 'VCF-PROCESSING	START' in line:
#                 line_status['VCF_PROCESSING'] = 'running'
#             elif 'CONVERT-MERGED-TABLE-TO-VCF	END' in line:
#                 line_status['VCF_PROCESSING'] = 'completed'
#             elif 'VCF-PROCESSING ERROR' in line:
#                 line_status['VCF_PROCESSING'] = 'error'
                
#             elif 'VCF-ANNOTATION	START' in line:
#                 line_status['VCF_ANNOTATION'] = 'running'
#             elif 'VCF-ANNOTATION END' in line:
#                 line_status['VCF_ANNOTATION'] = 'completed'
#             elif 'VCF_ANNOTATION	ERROR' in line:
#                 line_status['VCF_ANNOTATION'] = 'error'

#     # Render the template with data
#     return render(request, 'Geneapp/workflow_details.html', {'entry': entry, 'progress_data': progress_data, 'line_status': line_status})





from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import os

def get_galog_log_content(log_directory):
    # List all files in the directory
    files = os.listdir(log_directory)
    
    # Filter for files ending with .galog.log
    galog_logs = [file for file in files if file.endswith(".galog.log")]

    # If there are galog logs, choose the first one (you can adjust this logic if needed)
    if galog_logs:
        galog_log_filename = galog_logs[0]  # Choose the first one
        galog_log_path = os.path.join(log_directory, galog_log_filename)

        # Read content of galog log file
        with open(galog_log_path, 'r') as file:
            galog_content = file.readlines()
        return galog_content
    else:
        return None

def workflow_details_view(request, Workflow_ID):
    # Get the UserHistory object
    entry = get_object_or_404(UserHistory, id=Workflow_ID)
    
    # Construct the file path dynamically based on the user's project name and workflow name
    base_path = "C:\\Users\\Tejas\\Desktop\\csv_mysql\\New_folder_3\\DjangoGeneAssure_31_12\\GeneAssure_FASTQC_LNX_main\\bin\\"
    project_path = entry.project.name.replace(" ", "_")  # Replace spaces with underscores
    sample_id = entry.sample_id.replace(" ", "_") 
    workflow_path = entry.workflow_name.replace(" ", "_")  # Replace spaces with underscores
    log_directory = os.path.join(base_path, project_path, sample_id, workflow_path, "LOGS")
    
    # Check if the directory exists
    if not os.path.exists(log_directory):
        # Render the template with a message indicating that the process is running and the file is not generated
        return render(request, 'Geneapp/workflow_details.html', {'entry': entry, 'message': 'Process is Running, File Not Generated..'})
    
    # List all files in the directory
    files = os.listdir(log_directory)
    
    # Filter for files ending with .trace.log and get the last one
    trace_logs = [file for file in files if file.endswith(".trace.log")]
    if trace_logs:
        trace_log_filename = sorted(trace_logs)[-1]  # Get the last one
        log_file_path = os.path.join(log_directory, trace_log_filename)
    else:
        log_file_path = None  # No .trace.log file found

    progress_data = []
    line_status = {}

    # Read the content of the log file
    with open(log_file_path, 'r') as file:
        log_content = file.readlines()

       
        # Append each line to progress_data and determine status
        for line in log_content:
            progress_data.append(line.strip())
            # Determine the status of each line
            if 'MAPPING	START' in line:
                line_status['MAPPING'] = 'running'
            elif 'MAPPING	END' in line:
                line_status['MAPPING'] = 'completed'
            elif 'MAPPING ERROR' in line:
                line_status['MAPPING'] = 'error'
                
            if 'BAM-PROCESSING	START' in line:
                line_status['BAM_PROCESSING'] = 'running'
            elif 'BAM-PROCESSING	END' in line:
                line_status['BAM_PROCESSING'] = 'completed'
            elif 'BAM-PROCESSING ERROR' in line:
                line_status['BAM_PROCESSING'] = 'error'
                
            if 'VCF CALLING	START' in line:
                line_status['VCF_CALLING'] = 'running'
            elif 'VCF-FILTERATION	END' in line:
                line_status['VCF_CALLING'] = 'completed'
            elif 'VCF CALLING ERROR' in line:
                line_status['VCF_CALLING'] = 'error'
                
            elif 'VCF-PROCESSING	START' in line:
                line_status['VCF_PROCESSING'] = 'running'
            elif 'CONVERT-MERGED-TABLE-TO-VCF	END' in line:
                line_status['VCF_PROCESSING'] = 'completed'
            elif 'VCF-PROCESSING ERROR' in line:
                line_status['VCF_PROCESSING'] = 'error'
                
            elif 'VCF-ANNOTATION	START' in line:
                line_status['VCF_ANNOTATION'] = 'running'
            elif 'VCF_ANNOTATION	END' in line:
                line_status['VCF_ANNOTATION'] = 'completed'
            elif 'VCF_ANNOTATION	ERROR' in line:
                line_status['VCF_ANNOTATION'] = 'error'
                
            # Get content of galog log file
    galog_content = get_galog_log_content(log_directory)
    
    # Save the status to the last_status field of the UserHistory object
    last_status = line_status.get('VCF_ANNOTATION', 'RUNNING')
    entry.last_status = last_status
    entry.save()
    
    # Fetch file paths for output files
    fastqc1_path = os.path.join(base_path, project_path, sample_id, workflow_path, "REPORTS", "FASTQC_REPORT", "SRR19544453_1_fastqc.html")
    fastqc2_path = os.path.join(base_path, project_path, sample_id, workflow_path, "REPORTS", "FASTQC_REPORT", "SRR19544453_2_fastqc.html")
    
    multiqc_path = os.path.join(base_path, project_path, sample_id, workflow_path, "REPORTS", "MULTIQC_REPORT", "GA_Multiqc_Report.html")
    
    bam_path = os.path.join(base_path, project_path, sample_id, workflow_path, "BAMS", f"test_workflow.ga_map.bam")
    bai_path = os.path.join(base_path, project_path, sample_id, workflow_path, "BAMS", f"test_workflow.ga_map.bam.bai")
    
    vcf_path = os.path.join(base_path, project_path, sample_id, workflow_path, "VCFS", "GAVCF1", f"test_workflow.gavcf1.vcf.gz")
    

   
    # Render the template with data
    return render(request, 'Geneapp/workflow_details.html', {
        'entry': entry,
        'progress_data': progress_data,
        'line_status': line_status,
        'galog_content': galog_content,
        'fastqc1_path': fastqc1_path,
        'fastqc2_path': fastqc2_path,
        'multiqc_path': multiqc_path,
        'bam_path': bam_path,
        'bai_path': bai_path,
        'vcf_path': vcf_path,
    })





from django.http import FileResponse

def view_file(request, file_path):
    try:
        # Open the file and serve its contents as a response
        with open(file_path, 'r') as file:
            # Read the content of the file
            content = file.read()
        
        # Return the content in a HttpResponse with 'text/html' content type
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)

def download_file(request, file_path):
    # Open the file and serve it for download
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response

import urllib.parse

def download_galog(request):
    # Get the GALOG content from the request
    galog_content_param = request.GET.get('galog_content', '')
    
    # Decode the URL-encoded galog_content
    galog_content = urllib.parse.unquote(galog_content_param)
    
    if galog_content:
        # Split the galog_content into lines
        galog_lines = galog_content.split('\\n')
        
        # Remove the leading "', '" from each line
        galog_lines = [line[3:] if line.startswith("', '") else line for line in galog_lines]
        
        # Concatenate the lines with newline character
        galog_content_formatted = '\n'.join(galog_lines)
        
        # Set up the response
        response = HttpResponse(galog_content_formatted, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="galog_file.txt"'
        return response
    else:
        # Return an error response if no GALOG content is provided
        return HttpResponse("Error: No GALOG content provided.")






import os
import csv
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import UserHistory


# def workflow_details_view2(request, Workflow_ID):
#     entry = get_object_or_404(UserHistory, id=Workflow_ID)

#     # Construct the file path dynamically based on the user's project name, sample ID, and workflow name
#     base_path = "C:\\Users\\Tejas\\Desktop\\csv_mysql\\New_folder_3\\DjangoGeneAssure_31_12\\GeneAssure_FASTQC_LNX_main\\bin"
#     project_path = entry.project.name.replace(" ", "_")
#     sample_id = entry.sample_id.replace(" ", "_")
#     workflow_path = entry.workflow_name.replace(" ", "_")
#     file_path = os.path.join(base_path, project_path, sample_id, workflow_path, "A_V", "downloaded_file2.txt")

#     # Read the content of the text file and parse it into a list of dictionaries
#     file_data = []
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file, delimiter='\t')
#             for row in reader:
#                 file_data.append(row)

#     # Define the igv_options dictionary (unchanged)
#     igv_options = {
#         'genome': 'hg38',
#         'locus': 'chr8:127,736,588-127,739,371',
#         'tracks': [
#             {
#                 'name': "Color by attribute biotype",
#                 'type': "annotation",
#                 'format': "gff3",
#                 'displayMode': "expanded",
#                 'height': 300,
#                 'url': "https://s3.amazonaws.com/igv.org.genomes/hg38/Homo_sapiens.GRCh38.94.chr.gff3.gz",
#                 'indexURL': "https://s3.amazonaws.com/igv.org.genomes/hg38/Homo_sapiens.GRCh38.94.chr.gff3.gz.tbi",
#                 'visibilityWindow': 1000000,
#                 'colorBy': "biotype",
#                 'colorTable': {
#                     "antisense": "blueviolet",
#                     "protein_coding": "blue",
#                     "retained_intron": "rgb(0, 150, 150)",
#                     "processed_transcript": "purple",
#                     "processed_pseudogene": "#7fff00",
#                     "unprocessed_pseudogene": "#d2691e",
#                     "*": "black"
#                 }
#             }
#         ]
#     }

#     # Display the template with the processed data for the particular Workflow_ID
#     return render(request, 'Geneapp/workflow_details2.html', {'entry': entry, 'igv_options': igv_options, 'file_data': file_data})



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def workflow_details_view2(request, Workflow_ID):
    entry = get_object_or_404(UserHistory, id=Workflow_ID)

    base_path = "C:\\Users\\Tejas\\Desktop\\csv_mysql\\New_folder_3\\DjangoGeneAssure_31_12\\GeneAssure_FASTQC_LNX_main\\bin"
    project_path = entry.project.name.replace(" ", "_")
    sample_id = entry.sample_id.replace(" ", "_")
    workflow_path = entry.workflow_name.replace(" ", "_")
    file_path = os.path.join(base_path, project_path, sample_id, workflow_path, "A_V", "trim_SRR7002370_actionable_variants.txt")

    file_data = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                file_data.append(row)

    # Search functionality
    search_query = request.GET.get('q', '')

    # Filter data based on search query for all columns
    if search_query:
        filtered_data = []
        for row in file_data:
            for key, value in row.items():
                if search_query.lower() in str(value).lower():
                    filtered_data.append(row)
                    break  # Add the row once a match is found in any column
    else:
        filtered_data = file_data

    # Paginate the filtered file data
    paginator = Paginator(filtered_data, 50)  # Show 1000 rows per page
    page_number = request.GET.get('page')
    try:
        file_data_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        file_data_paginated = paginator.page(1)
    except EmptyPage:
        file_data_paginated = paginator.page(paginator.num_pages)

    # Define the igv_options dictionary
    # igv_options = {
    #     'genome': 'hg38',
    #     'locus': 'chr8:127,736,588-127,739,371',
    #     'tracks': [
    #         {
    #             "type": "variant",
    #             "format": "vcf",
    #             "url": "https://tss3bucket1.s3.amazonaws.com/test_workflow.vcf.gz",
    #             "indexURL": "https://tss3bucket1.s3.amazonaws.com/test_workflow.vcf.gz.tbi",
    #             "name": "Variants",
    #         },
    #         {
    #            'type': "alignment",
    #             'format': "bam",
    #             'name': "NA12889",
    #             'url': "https://tss3bucket1.s3.amazonaws.com/test_workflow.ga_map.bam",
    #             'indexURL': "https://tss3bucket1.s3.amazonaws.com/test_workflow.ga_map.bam.bai", 
    #         }
    #     ]
    # }
    
    igv_options = {
        'genome': 'hg38',
        'locus': 'chr8:127,736,588-127,739,371',
        'tracks': [
            {
                    'name': "Color by attribute biotype",
                    'type': "variants",
                    'format': "vcf",
                    'displayMode': "expanded",
                    'height': 300,
                    'url': "https://tss3bucket1.s3.amazonaws.com/test_workflow.vcf.gz",
                    'indexURL': "https://tss3bucket1.s3.amazonaws.com/test_workflow.vcf.gz.tbi",
                    'visibilityWindow': 1000000,
                    'colorBy': "biotype",
                    'colorTable': 
                        {
                            "antisense": "blueviolet",
                            "protein_coding": "blue",
                            "retained_intron": "rgb(0, 150, 150)",
                            "processed_transcript": "purple",
                            "processed_pseudogene": "#7fff00",
                            "unprocessed_pseudogene": "#d2691e",
                            "*": "black"
                        }
                
            }
        ]
    }
    
    return render(request, 'Geneapp/workflow_details2.html', {
        'entry': entry,
        'igv_options': igv_options,
        'file_data_paginated': file_data_paginated,
        'search_query': search_query,
    })
