const wol = require('wol');

const process = require('process');
const spawn = require('child_process').spawnSync;

const Modes = {
    SWITCH_TO_TV: 'switch_to_tv',
    SWITCH_TO_MONITORS: 'switch_to_monitors',
    SWITCH_TO_UPPER_ONLY: 'switch_to_upper'
};

async function main() {
    const mode = _validateAndGetMode(process.argv[2]);
    const lgtvConfig = require('./lgtv_config.json')

    switch (mode) {
        case Modes.SWITCH_TO_TV:
            await _mainSwitchToTv(lgtvConfig)
            return;

        case Modes.SWITCH_TO_MONITORS:
            await _mainSwitchToMonitors(lgtvConfig)
            return;

        case Modes.SWITCH_TO_UPPER_ONLY:
            await _mainSwitchToUpper();
            return;
    }
}

function _validateAndGetMode(mode) {
    for (const m in Modes) {
        if (Modes[m] == mode) {
            return Modes[m];
        }
    }
    throw `Unknown mode "${mode}".`;
}

async function _mainSwitchToTv(lgtvConfig) {
    wol.wake(lgtvConfig['tv_mac'], (err) => {
        if (err) {
            console.error(err);
            throw 'Wake on LAN failed, see above error for details.';
        }
    });

    // LG seems to have updated their API and now this doesn't work. RIP
    // let lgtv = await _tryLgtvConnect(lgtvConfig['tv_ip'])

    // await _tryLgtvRequest(lgtv, 'ssap://tv/switchInput', {inputId: 'HDMI_2'});
    // lgtv.disconnect();

    // // dc2.exe throws an ERROR_GEN_FAILURE without some extra time to swap inputs, maybe something to do with HDR?
    // await _asyncSleep(2000);
    _swapDisplays('dc2_tv_config.xml');

    // The websocket takes a while to disconnect, which keeps the console open for a bit, this is a hack to skip that
    process.exit(0);
}

async function _mainSwitchToMonitors(lgtvConfig) {
    _swapDisplays('dc2_monitors_config.xml');

    // RIP
    // let lgtv = await _tryLgtvConnect(lgtvConfig['tv_ip'])

    // await _tryLgtvRequest(lgtv, 'ssap://tv/switchInput', {inputId: 'HDMI_4'});

    // // lgtv doesn't wait until the command finishes, so give it a bit of time to finish before turning off
    // await _asyncSleep(2000);
    // await _tryLgtvRequest(lgtv, 'ssap://system/turnOff');
    // lgtv.disconnect();

    process.exit(0);
}

async function _mainSwitchToUpper() {
    _swapDisplays('dc2_upper_only_config.xml');
    process.exit(0);
}

async function _tryLgtvConnect(tvIp) {
    return new Promise(resolve => {
        const url = `ws://${tvIp}:3000`;
        console.log(`Trying to connect to LG TV at ${url}...`)

        // lgtv2 (through the websocket) will connect successfully whenever it can, even if the TV is in the middle of
        // turning on. Eventually if it really can't connect it'll fail with the "error" event
        let lgtv = require('lgtv2')({
            url: url
        });

        lgtv.on('error', (err) => {
            console.error(err);
            throw err;
        });

        lgtv.on('connect', () => {
            console.log(`Connected to LG TV at ${url}`);
            resolve(lgtv);
        });
    });
}

async function _tryLgtvRequest(lgtv, url, payload) {
    return new Promise(resolve => {
        console.log(`Trying to send request to url ${url}...`)

        lgtv.request(url, payload ? JSON.stringify(payload) : null, (err, resp) => {
            if (err) {
                throw err;
            }

            // Sometimes lgtv responses don't have payloads
            if (resp.payload && resp.payload.errorCode) {
                throw `Request failed: ${resp.payload.errorText}`;
            }

            console.log(`Request to url ${url} complete`)
            resolve(resp)
        });
    });
}

function _swapDisplays(config) {
    // In testing, this really didn't like full paths for -configure for some reason, maybe escaping weirdness?
    spawn('E:\\Programs\\dc2.exe', [`-configure=${config}`]);

    // Display Changer has some annoyances where the audio doesn't swap with the display, this works around that
    spawn('cmd.exe', ['/c', 'net stop audiosrv']);
    spawn('cmd.exe', ['/c', 'net start audiosrv']);
}

async function _asyncSleep(timeout) {
    return new Promise(resolve => {
        setTimeout(() => resolve(), timeout);
    });
}

main();