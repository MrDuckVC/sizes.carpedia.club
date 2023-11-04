## **Completely configure the server**

To set up production server completely run this command:
`bash setup.sh`

If you want to install only one service, read text below.

## **Docker Installation**

To install docker on ubuntu, run the following command:
`bash docker.sh`
1. When asked 'Which services should be restarted?', press enter.
Docker installation is complete.

## **Nginx Installation**

To install nginx on ubuntu, run the following command:
`bash nginx.sh`
1. When asked 'Which services should be restarted?', press enter.
2. When ask for email, enter your email address (example@email.com) and press enter.
3. When asked for terms of service, enter 'Y' and press enter.
4. When asked for sharing email, enter 'N' and press enter.
5. When asked for domain name, enter your domain name (www.example.com) and press enter.
Nginx with certbot installation is complete.
