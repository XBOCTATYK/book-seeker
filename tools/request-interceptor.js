// use this request to acquire request url with all params
const intercept = () => {
  const open = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url, ...rest) {
    console.log(url)
    return open.call(this, method, url, ...rest);
  };
}

intercept()
