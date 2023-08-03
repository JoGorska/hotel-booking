const Pty = require('node-pty');
const fs = require('fs');

exports.install = function () {

    ROUTE('/');
    WEBSOCKET('/', socket, ['raw']);

};

function socket() {

    this.encodedecode = false;
    this.autodestroy();

    this.on('open', function (client) {

        // Spawn terminal
        client.tty = Pty.spawn('python3', ['run.py'], {
            name: 'xterm-color',
            cols: 80,
            rows: 24,
            cwd: process.env.PWD,
            env: process.env
        });

        client.tty.on('exit', function (code, signal) {
            client.tty = null;
            client.close();
            console.log("Process killed");
        });

        client.tty.on('data', function (data) {
            client.send(data);
        });

    });

    this.on('close', function (client) {
        if (client.tty) {
            client.tty.kill(9);
            client.tty = null;
            console.log("Process killed and terminal unloaded");
        }
    });

    this.on('message', function (client, msg) {
        client.tty && client.tty.write(msg);
    });
}

if (process.env.CREDS === true ) {
    const json_creds = `{
        "type": ${process.env.type},
        "project_id": ${process.env.project_id},
        "private_key_id": ${process.env.private_key_id},
        "private_key": ${process.env.private_key},
        "client_email": ${process.env.client_email},
        "client_id": ${process.env.client_id},
        "auth_uri": ${process.env.auth_uri},
        "token_uri": ${process.env.token_uri},
        "auth_provider_x509_cert_url": ${process.env.auth_provider_x509_cert_url},
        "client_x509_cert_url": ${process.env.client_x509_cert_url}
    }`
    console.log("Creating creds.json file.");
    fs.writeFile('creds.json', json_creds, 'utf8', function (err) {
        if (err) {
            console.log('Error writing file: ', err);
            socket.emit("console_output", "Error saving credentials: " + err);
        }
    });
}