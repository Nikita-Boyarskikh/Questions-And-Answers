cp ./nginx.conf ./tmp.conf && \
echo "#app='$PROJECT_NAME'#" >> ./tmp.conf && \
echo "#root='$PROJECT_ROOT'#" >> ./tmp.conf && \
unlink /etc/nginx/sites-enabled/$PROJECT_NAME.conf && \
unlink /etc/nginx/sites-enabled/default && \
cat ./tmp.conf | perl ./write_nginx_config.pl > /etc/nginx/sites-available/$PROJECT_NAME.conf && \
ln -s /etc/nginx/sites-available/$PROJECT_NAME.conf /etc/nginx/sites-enabled/$PROJECT_NAME.conf && \
mv ./proxy_params /etc/nginx/sites-available/proxy_params && \
rm ./tmp.conf ./nginx.conf ./write_nginx_config.pl ./deploy.sh