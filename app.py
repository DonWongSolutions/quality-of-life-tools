from flask import Flask, request, jsonify, render_template_string, render_template

app = Flask(__name__)


@app.route('/')
def homepage():  # put application's code here
    return render_template('index.html')

@app.route('/rproxy')
def rproxy():  # put application's code here
    return render_template('rproxy.html')


@app.route('/generate_preview', methods=['POST'])
def generate_preview():
    server_name = request.form.get('serverName', '')
    localport = request.form.get('localport', '')
    enable_pph = request.form.get('enablePph') == 'on'
    port = request.form.get('port', '')
    serveradmin = request.form.get('serverAdmin', '')
    sslfile = request.form.get('SSLFile', '')
    sslkey = request.form.get('SSLKey', '')
    accesslogname = request.form.get('accesslogname', '')
    errorlogname = request.form.get('errlogname', '')
    redirect = request.form.get('httpredirection') == 'on'

    # Simple template for Apache configuration
    config_preview = f"""
    <VirtualHost *:{port}>
        ServerName {server_name}
        ServerAdmin {serveradmin}
        {'ProxyPreserveHost On' if enable_pph else 'ProxyPreserveHost Off'}
        ProxyPass / http://localhost:{localport}/
        ProxyPassReverse / http://localhost:{localport}/
        
        {'SSLEngine on' if port == '443' else 'SSLEngine off'}
        {f'SSLCertificateFile {sslfile}' if port == '443' else ''}
        {f'SSLCertificateKeyFile {sslkey}' if port == '443' else ''}
        
        ErrorLog ${{APACHE_LOG_DIR}}/{errorlogname}.log
        CustomLog ${{APACHE_LOG_DIR}}/{accesslogname}.log combined
    </VirtualHost>
    """

    extendedpreview = f"""
    <VirtualHost *:80>
        ServerName {server_name}
        ServerAdmin {serveradmin}
        Redirect permanent / https://{server_name}/
    </VirtualHost>
    """

    if redirect:
        return extendedpreview+config_preview
    else:
        return config_preview

if __name__ == '__main__':
    app.run()
