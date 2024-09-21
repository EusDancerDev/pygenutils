#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:00:51 2024

@author: jonander

**Goal**
Make audio transcriptions using preferently free software
Easiest way is using IBM Watson Cloud services (IBM Watsonx),
available through Anaconda.
The service or resource to accomplish the task is 'Speech To Text'
"""

#----------------#
# Import modules # 
#----------------#

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#-----------------------#
# Import custom modules # 
#-----------------------#

from pyutils.files_and_directories.file_and_directory_paths import find_files_by_ext
from pyutils.strings import string_handler, information_output_formatters

# Create aliases #
#----------------#

ext_adder = string_handler.ext_adder
modify_obj_specs = string_handler.modify_obj_specs

print_format_string = information_output_formatters.print_format_string

#------------------#
# Define functions # 
#------------------#

def save_transcription_in_file(transcript, relative_path_noext, ext="txt"):
    
    # Add the extension to the input file #
    relative_path = ext_adder(relative_path_noext, ext)
    
    # Create the file object #
    file_object = open(relative_path, "w")
    
    # Write the transcription to the file #
    print_format_string(saving_transcription_str, relative_path)
    
    file_object.write(transcript)
    file_object.close()
    
    # If the execution has reached the end with no errors, print a confirmation message #
    print("Transcription successfully writt.")
    

#-------------------#
# Define parameters #
#-------------------#

# File extensions #
file2transcript_ext = "wav"

# Relative paths #
files2transcribe_path = "/home/jonander/Documents/04-Ikasketak/04-Ikastaroak/"\
                        "Deusto_Formacion/Curso_superior_Python/teoria/moduluak/Tema_5/"

files2transcribe_list = find_files_by_ext(file2transcript_ext,
                                          files2transcribe_path, 
                                          top_path_only=True)

# Output informartion strings #
transcription_result_str = """File : {}
Transcription:
    
{}"""

saving_transcription_str = "Saving transcription to file {}"

# Transcription controls #
print_transcription = False
save_transcription = False

# IBM Watson Cloud's Speech To Text service's keys #
"""
Steps to get the API Key and 'Speech To Text' service ID
--------------------------------------------------------
1. Open Anaconda Navigator and select IBM Watsonx and log in
2. At the top-left corner, click into the four horizontal parallel lines.
    2.1 Unfold the 'Administration' menu and click the 'Access (IAM)' option.
        Another tab will be opened, redirecting to IBM Cloud
    2.2 At IBM Cloud, check whether the mentioned resource -Speech To Text'-
        is activated, at the resources list.
        2.2.1 In the leftmost shrinked panel, click into the bulletpoint icon 
              (third one, starting from the upmost four horizontal parallel
                lines icon). The resources list will show.
        2.2.2 The section that this service belongs to is 'AI / Machine Learning'
              If the service does not appear, search through the catalog
              (upmost main bar, at the right of the search bar) and create it.
    2.3 When checked or created, at the resource list, click on the service
    2.4 The API Key and service ID are contained in the 'Credentials' tag;
        the service ID is contained in the URL, after the last forward slash.
"""

# Define both the API_KEY and SERVICE_ID here
    
#----------------#
# Operation part # 
#----------------#

# Set up authentication #
#-----------------------#

url = f"https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/{SERVICE_ID}"

authenticator = IAMAuthenticator(API_KEY)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(url)

# Loop through the file list #
#----------------------------#

for audio_file in files2transcribe_list:    
    with open(audio_file, "rb") as audio:
        
        # Transcribe the audio file #
        response = speech_to_text.recognize(audio=audio,
                                            content_type=f"audio/{file2transcript_ext}")
        
    # Save or print transcription as chosen #
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    
    transcript = response.result['results'][0]['alternatives'][0]['transcript']
    arg_list = [audio_file, transcript]
    
    transcript_file_name = modify_obj_specs(audio_file, 
                                            "name_noext",
                                            str2add="_transcription")
    
    if print_transcription: 
        print_format_string(transcription_result_str(arg_list))
    
    if save_transcription:
        save_transcription_in_file(transcript, transcript_file_name)
        
    if (not print_transcription and not save_transcription):
        print("No transcription printing nor saving chosen")
