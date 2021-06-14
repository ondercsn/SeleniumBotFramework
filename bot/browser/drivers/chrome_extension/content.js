/*
var chromeplugin1 = {description : "Portable Document Format",filename : "internal-pdf-viewer",length : 1,name : "Chromium PDF Plugin"}
var chpl2 = {0: MimeType, application/x-google-chrome-pdf: MimeType, name: "Chromium PDF Plugin", filename: "internal-pdf-viewer", description: "Portable Document Format", length: 1}
Object.defineProperty(navigator, 'plugins', {get: () => [ 1,2,3 ]} );
*/
var customScript = `
var chvals = {
  app: {
    isInstalled: false,
  },
  webstore: {
    onInstallStageChanged: {},
    onDownloadProgress: {},
  },
  runtime: {
    PlatformOs: {
      MAC: 'mac',
      WIN: 'win',
      ANDROID: 'android',
      CROS: 'cros',
      LINUX: 'linux',
      OPENBSD: 'openbsd',
    },
    PlatformArch: {
      ARM: 'arm',
      X86_32: 'x86-32',
      X86_64: 'x86-64',
    },
    PlatformNaclArch: {
      ARM: 'arm',
      X86_32: 'x86-32',
      X86_64: 'x86-64',
    },
    RequestUpdateCheckStatus: {
      THROTTLED: 'throttled',
      NO_UPDATE: 'no_update',
      UPDATE_AVAILABLE: 'update_available',
    },
    OnInstalledReason: {
      INSTALL: 'install',
      UPDATE: 'update',
      CHROME_UPDATE: 'chrome_update',
      SHARED_MODULE_UPDATE: 'shared_module_update',
    },
    OnRestartRequiredReason: {
      APP_UPDATE: 'app_update',
      OS_UPDATE: 'os_update',
      PERIODIC: 'periodic',
    },
  },
}

Object.defineProperty(navigator, 'webdriver', {get: () => false});
Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
Object.defineProperty(navigator, 'BuildID', {get: () => undefined});
Object.defineProperty(navigator, 'Sec-fetch-user', {get: () => "?1"});
Object.defineProperty(navigator, 'Sec-fetch-site', {get: () => "same-origin"});
Object.defineProperty(navigator, 'Sec-fetch-mode', {get: () => "navigate"});

Object.defineProperty(navigator, "hardwareConcurrency", {
  set: function () { return "1"; }, 
  get: function () { return "1"; } 
});


['height', 'width'].forEach(property => {
  // store the existing descriptor
  const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);

  // redefine the property with a patched descriptor
  Object.defineProperty(HTMLImageElement.prototype, property, {
    ...imageDescriptor,
    get: function() {
      // return an arbitrary non-zero dimension if the image failed to load
      if (this.complete && this.naturalHeight == 0) {
        return 20;
      }
      // otherwise, return the actual dimension
      return imageDescriptor.get.apply(this);
    },
  });
});

const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');
Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
  ...elementDescriptor,
  get: function() {
    if (this.id === 'modernizr') {
        return 1;
    }
    return elementDescriptor.get.apply(this);
  },
});


var originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = parameters => (
  parameters.name === 'notifications' ?
    Promise.resolve({ state: Notification.permission }) :
    originalQuery(parameters)
);

res = document.getElementById ('resolutionNumber');
res.innerHTML = width + " X " + height;



unBotDetection = function () {
    var documentDetectionKeys = [
        "__webdriver_evaluate",
        "__selenium_evaluate",
        "__webdriver_script_function",
        "__webdriver_script_func",
        "__webdriver_script_fn",
        "__fxdriver_evaluate",
        "__driver_unwrapped",
        "__webdriver_unwrapped",
        "__driver_evaluate",
        "__selenium_unwrapped",
        "__fxdriver_unwrapped",
    ];

    var windowDetectionKeys = [
        "_phantom",
        "__nightmare",
        "_selenium",
        "callPhantom",
        "callSelenium",
        "_Selenium_IDE_Recorder",
    ];

    for (const windowDetectionKey in windowDetectionKeys) {
        const windowDetectionKeyValue = windowDetectionKeys[windowDetectionKey];
        if (window[windowDetectionKeyValue]) {
            return true;
        }
    };
    for (const documentDetectionKey in documentDetectionKeys) {
        const documentDetectionKeyValue = documentDetectionKeys[documentDetectionKey];
        if (window['document'][documentDetectionKeyValue]) {
            return true;
        }
    };

    for (const documentKey in window['document']) {
        if (documentKey.match(/\$[a-z]dc_/) && window['document'][documentKey]['cache_']) {
            return true;
        }
    }

    if (window['external'] && window['external'].toString() && (window['external'].toString()['indexOf']('Sequentum') != -1)) return true;

    if (window['document']['documentElement']['getAttribute']('selenium')) return true;
    if (window['document']['documentElement']['getAttribute']('webdriver')) return true;
    if (window['document']['documentElement']['getAttribute']('driver')) return true;

    return false;
};


`;
/*

Object.defineProperty(navigator, "platform", {
  set: function () { return "Linux armv8I"; }, 
  get: function () { return "Linux armv8I"; } 
});


*/

var script = document.createElement('script');
script.appendChild(document.createTextNode(customScript));
(document.head || document.documentElement).appendChild(script);
script.parentNode.removeChild(script);



