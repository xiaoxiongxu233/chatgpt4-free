window.dc674d = window.fetch;
const e = window.navigator,
    n = {
        a: e.userAgent,
        b: e.platform,
        c: e.language,
        d: e.cookieEnabled,
        e: e.onLine,
        f: e.doNotTrack,
        g: e.javaEnabled(),
        i: e.appName,
        j: e.mediaDevices,
        k: e.appCodeName,
        l: e.product,
        m: e.productSub,
        n: e.hardwareConcurrency,
        o: e.maxTouchPoints,
        p: e.vendor,
        q: e.vendorSub,
        r: e.oscpu,
        s: e.buildID,
        t: e.mimeTypes,
        u: e.plugins
    };

function t(e) {
    return e.replace(/[A-Z0-9+/=]/gi, e => "nea97XU2LmOy1tD40jo-JvRhpbuFfgT3CKW6NIwArPqQlxskZ5c8zd.YVMiEBSHG=" ["ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".indexOf(e)])
}

function a(e) {
    const n = Object.keys(e);
    for (let e = n.length - 1; e > 0; e--) {
        const t = Math.floor(Math.random() * (e + 1));
        [n[e], n[t]] = [n[t], n[e]]
    }
    const t = {};
    for (let a = 0; a < n.length; a++) t[n[a]] = e[n[a]];
    return t
}
const o = e => btoa(String.fromCharCode.apply(null, e));
async function r() {
    return plain_sec = JSON.stringify({
        ...a(n),
        timestamp: Date.now()
    }), t(await o(d(plain_sec, "chatgpt.rip.6675636b206f6666202122a72425262f28293d3f")))
}

function i(e) {
    let n = [...Array(256).keys()],
        t = 0;
    for (let a = 0; a < 256; a++) {
        t = (t + n[a] + e[a % e.length]) % 256;
        let o = n[a];
        n[a] = n[t], n[t] = o
    }
    return n
}

function* c(e) {
    let n = 0,
        t = 0;
    for (;;) {
        let a = e[t = (e[n = (1 + n) % 256] + t) % 256];
        e[t] = e[n], e[n] = a, yield e[(e[n] + e[t]) % 256]
    }
}

function d(e, n) {
    let t = [...e].map(e => e.charCodeAt()),
        a = c(i([...n].map(e => e.charCodeAt())));
    return t.map(e => e ^ a.next().value)
}

function u(e, n) {
    let t = c(i([...n].map(e => e.charCodeAt())));
    return e.map(e => String.fromCharCode(e ^ t.next().value)).join("")
}
window.fetch = async function(e, n) {
    return shape_info = await r(), window.dc674d(e, {
        ...n,
        headers: {
            ...{
                "x-shape-info": shape_info
            },
            ...n && n.headers || {}
        }
    })
};