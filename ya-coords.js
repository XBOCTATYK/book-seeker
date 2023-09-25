// you can use this script to aquire 4 coordinate points at yandex maps
const oldfetch = window.fetch;

window.fetch = function(...args) {
    const t = decodeURIComponent(args[1].body).match(/\[\[[^a-z]+\]\]/);
    console.log((JSON.parse(t && t[t.length - 1]))?.join(','));
    return oldfetch(...args)
}
