## Configuration

1.  Go to **Website \> Configuration \> Settings**
2.  In the **Website Info** section, find the **llms.txt Content** field
3.  Enter the content you want to serve at /llms.txt
4.  Save the settings

## Usage

After configuration, the /llms.txt file will be available at your
website root:

- If content is configured: The configured content will be served
- If content is empty: A default content will be generated based on your
  website information

Example content format:

    # Your Website — Information for LLMs

    ## Company
    - About: https://yourdomain.com/aboutus
    - Contact: https://yourdomain.com/contactus

    ## Services
    - Service 1: https://yourdomain.com/service1
    - Service 2: https://yourdomain.com/service2

    ## Content
    - Blog: https://yourdomain.com/blog
