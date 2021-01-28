#!/usr/bin/env python

import json
import requests # pylint: disable=import-error
from google.cloud import recommender
import googleapiclient.discovery # pylint: disable=import-error
from google.api_core import exceptions
import sys

def main():
    """
    Central brain of the script. Executes other functions.
    """

    # Generate a list of project numbers in the GCP Organization
    project_numbers = get_projects()
    
    # Takes the project numbers and finds the inactive service accounts
    get_sa_insights(project_numbers)

def get_sa_insights(project_numbers):
    """
    Gathers the Service Account insights from IAM recommender.
    """
    # Create IAM Recommender client
    recommender_client = recommender.RecommenderClient()

    findings=[]
    # Iterate through project nums to generate SA findings per project
    for project_num in project_numbers:
        try:
            sa_insights = recommender_client.list_insights(parent=f"projects/{project_num}/locations/global/insightTypes/google.iam.serviceAccount.Insight")
        except exceptions.PermissionDenied as perm:
            print(f"{perm}")
            sys.exit(1)
        for insight in sa_insights:
            email = insight.content["email"]
            inactive_sa = json.dumps(
                { "service_account_email" : email, 
                "project_number" : project_num }
            )
            print(inactive_sa)


def get_projects():
    """
    Gets a list of project numbers
    """
    service = create_service()

    # List available projects
    try:
        request = service.projects().list()
    except:
        print("Could not list projects. Check your permissions.")

    # Collect all the projects
    projects = []
    # Paginate through the list of all available projects
    while request is not None:
        response = request.execute()

        projects.extend(response.get('projects', []))

        request = service.projects().list_next(request, response)

    # For each project, extract the project number
    project_numbers = []
    for project in projects:
        project_num = project['projectNumber']

        project_numbers.append(project_num)
    
    return project_numbers


def create_service():
    """
    Creates the GCP Cloud Resource Service
    """
    return googleapiclient.discovery.build('cloudresourcemanager', 'v1')

if __name__ == "__main__":
    main()
