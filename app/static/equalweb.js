window.interdeal = {
    "sitekey": "1e3d0e1486615ccb29aaac018279ea47",
    "Position": "Right",
    "Menulang": "EN-GB",
    "domains": {
        "js": "https://cdn.equalweb.com/",
        "acc": "https://access.equalweb.com/"
    },
    "btnStyle": {
        "vPosition": [
            "80%",
            null
        ],
        "scale": [
            "0.8",
            "0.8"
        ],
        "icon": {
            "type": 7,
            "shape": "semicircle",
            "outline": false
        },
        "color": {
            "main": "#6E7577"
        }
    }
};
(function(doc, head, body){
	var coreCall             = doc.createElement('script');
	coreCall.src             = 'https://cdn.equalweb.com/core/2.1.8/accessibility.js';
	coreCall.defer           = true;
	coreCall.integrity       = 'sha512-tA0/58RaxqQMY+p5wW7LgZM88ckav7DG0iT6VEUqGVyFvH6PcFkmMVuWQgqftDp3BYYHxjeYTAX14Ct7DS/fRQ==';
	coreCall.crossOrigin     = 'anonymous';
	coreCall.setAttribute('data-cfasync', true );
	body? body.appendChild(coreCall) : head.appendChild(coreCall);
})(document, document.head, document.body);