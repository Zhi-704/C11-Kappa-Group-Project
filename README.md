# Liverpool Natural History Museum Plant Monitoring System

## Overview

Welcome to the Liverpool Natural History Museum Plant System repository. This repository contains the all the code, documentation and resources required to monitor and analyze the health of plants in the botanical wing of the museum. The system collects real-time data through an API from a variety of sensors placed next to each plant. This data is used for long-term storage and visualization, enabling museum staff to maintain and manage plant health effectively.

## Repository Structure

- `pipeline`: ETL (Extract, Transform, Load) pipeline that moves data from the API to the RDS (Relational Database Service).
- `archiver`: Component responsible for transferring old data from the RDS to an S3 bucket for long-term storage.
- `dashboard`: Interface designed for staff members to monitor and manage plant health.
- `terraform`: Infrastructure as Code (IaC) tool for provisioning and managing AWS resources and services.
- `diagrams`: Contains relevant diagrams such as ERD (Entity-Relationship Diagrams) and architecture diagrams.
- `.github`: GitHub-specific files required for repository configuration, such as workflows.

## Requirements

1. Clone this repository:
    ```sh
    git clone https://github.com/Zhi-704/C11-Kappa-Group-Project.git.
    ```

2. Navigate to the directory and install the required packages in the terminal:
    ```sh
    cd [PATH_TO_FOLDER]/C11-Kappa-Group-Project
    pip3 install -r local_requirements.txt
    ```

> [!NOTE]  
The `local_requirements.txt` file lists all necessary packages to run all folders locally. The other `requirements.txt` files are used for provisioning resources in AWS for Docker environments and image registry. If a folder encounters issues running the code, consider running `pip3 install -r requirements.txt` in the local folder to ensure all required packages are installed.


3. Run the schema.sql script found in the main repository to set up the database.
    ```sh
    sqlcmd -U [your_username] -d [your_database] -f schema.sql
    ```

## Secrets/Authentication

> [!IMPORTANT]  
> To run these scripts, the following details must be provided in an `.env` file within their respective folders. These credentials are sensitive and should NOT be shared.

Ensure you create an `.env` file in each relevant folder and include the necessary environment variables as outlined below:

| KEY | Affected Folders | Description |
| -------- | --------| --------|
|AWS_ACCESS_KEY|`terraform`| Authentication key for AWS used by Terraform to manage cloud resources.
|AWS_SECRET_KEY|`terraform`| Secret key for AWS used by Terraform for secure authentication.
|ACCESS_KEY|`archiver`,`dashboard`| Used to access the AWS system.
|SECRET_ACCESS_KEY|`archiver`, `dashboard`| Used for authentication for the AWS system.
|BUCKET_NAME|`archiver`, `dashboard`| Name of storage bucket (e.g., Amazon S3) where long-term data is stored.
|DB_HOST|`archiver`, `dashboard`, `terraform`| Host address of the database server used by the applications and Terraform.
|DB_USER|`archiver`, `dashboard`, `terraform`| Username for authenticating and accessing the database.
|DB_SCHEMA|`archiver`, `dashboard`, `terraform`| Refers to the database schema or namespace within the database.
|DB_PASSWORD|`archiver`, `dashboard`, `terraform`| Used for authentication for the user accessing the RDS.
|DB_PORT|`archiver`, `dashboard`, `terraform`| Port number on which the database server listens for connections.
|DB_NAME|`archiver`, `dashboard`, `terraform`| Name of the database used by the applications and Terraform.

## Pipeline (Local Set-Up)

To configure the ETL piepline for moving data from the API to the database, follow these steps:

1. Navigate to the `dashboard` directory:
    ```sh
    cd [PATH_TO_FOLDER]/C11-Kappa-Group-Project/pipeline
    ```

2. Create an `.env` file and configure its content with the correct information inside the folder. [For authentication and secrets setup, refer to the Secrets/Authentication section](#secretsauthentication)

3. Run the pipeline script:
    ```sh
    python3 pipeline.py
    ```


## Dashboard (Local Set-Up)

After setting up the pipeline, you can access the plant analytics dashboard locally by following these steps:

1. Navigate to the `dashboard` directory:
    ```sh
    cd [PATH_TO_FOLDER]/C11-Kappa-Group-Project/dashboard
    ```

2. Create an `.env` file and configure its content with the correct information inside the folder. [For authentication and secrets setup, refer to the Secrets/Authentication section](#secretsauthentication)

3. Run the dashboard application:
    ```sh
    streamlit run streamlit.py
    ```

4. Open a web browser and navigate to `http://localhost:5000`. The dashboard will display soil moisture and temperature data over time for all plants.

## Cloud Resources

To create all the necessary cloud resources and deploy the dashboard and pipeline online, follow these steps using Terraform:

1. Navigate to the `terraform` directory:
    ```sh
    cd [PATH_TO_FOLDER]/C11-Kappa-Group-Project/terraform
    ```
2. Initialise Terraform:
    ```sh
    terraform init
    ```
3. Apply Terraform to create the infrastructure
    ```sh
    terraform apply
    ```

4. (Optional) Destroy the infrastructure if needed:
    ```sh
    terraform destroy
    ```

> [!NOTE]  
> Ensure that your AWS credentials are configured properly before running the Terraform commands. This setup will create all required AWS resources for running the pipeline and dashboard.

## Archictecture Diagram

The project architecture is based on the diagram below:

![Architecture Diagram](https://github.com/Zhi-704/C11-Kappa-Group-Project/raw/main/diagrams/Architecture_Diagram.png)


## Database Schema

To view the database schema for the plant data, please refer to this Entity-Relationship Diagram (ERD). 


![ERD Diagram](https://github.com/Zhi-704/C11-Kappa-Group-Project/blob/main/diagrams/ERD_diagram.png)


> [!IMPORTANT]  
> This project monitors only changes in the `reading` table. All other data must be manually inserted during creation of the database or by informing the engineers.

## Dashboard Wireframe

Below is a wireframe of the plant analytics dashboard. This visual guide shows the layout and main components of the dashboard, which displays soil moisture and temperature data over time for all plants, as well as specific plants.

![Dashboard Wireframe](https://github.com/Zhi-704/C11-Kappa-Group-Project/blob/main/diagrams/Dashboard_Wireframe.png)
