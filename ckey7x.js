ha = function(a) {
    function b(a, b) {
        return ((a >> 1) + (b >> 1) << 1) + (1 & a) + (1 & b)
    }
    for (var c = [], d = 0; d < 64;) {
        c[d] = 0 | 4294967296 * Math.abs(Math.sin(++d))
    }
    var e = function(d) {
        for (var e, f, g, h, i = [], j = unescape(encodeURI(d)), k = j.length, l = [e = 1732584193, f = -271733879, ~e, ~f], m = 0; m <= k;) {
            i[m >> 2] |= (j.charCodeAt(m) || 128) << 8 * (m++%4)
        }
        for (i[d = (k + 8 >> 6) * a + 14] = 8 * k, m = 0; m < d; m += a) {
            for (k = l, h = 0; h < 64;) {
                k = [g = k[3], b(e = k[1], (g = b(b(k[0], [e & (f = k[2]) | ~e & g, g & e | ~g & f, e ^ f ^ g, f ^ (e | ~g)][k = h >> 4]), b(c[h], i[[h, 5 * h + 1, 3 * h + 5, 7 * h][k] % a + m]))) << (k = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, a, 23, 6, 10, 15, 21][4 * k + h++%4]) | g >>> 32 - k), e, f]
            }
            for (h = 4; h;) {
                l[--h] = b(l[h], k[h])
            }
        }
        for (d = ""; h < 32;) {
            d += (l[h >> 3] >> 4 * (1 ^ 7 & h++) & 15).toString(a)
        }
        return d
    };
    return e
} (16),
$xx = function(a, b, d, e, f, g) {
    if (magic = "123456", g.length < 3) {
        return "err"
    }
    if ("7." != g.substr(0, 2)) {
        return "err"
    }
    subver = g.substr(2),
    "1" == subver && (magic = "06fc1464"),
    "2" == subver && (magic = "4244ce1b"),
    "3" == subver && (magic = "77de31c5"),
    "4" == subver && (magic = "e0149fa2"),
    "5" == subver && (magic = "60394ced"),
    "6" == subver && (magic = "2da639f0"),
    "7" == subver && (magic = "c2f0cf9f");
    var f = f || parseInt( + new Date / 1000),
    e = ("" + e).charAt(0),
    h = ha(magic + b + f + "*#06#" + a);
    return h
};
ckey7 = function(platform_in, vid_in, std_in, test, tm_in, ver_in) {
    //var g = (new Date).getDay();
    //var d = "7." + (0 == g ? 7 : g);
    var i = $xx(platform_in, vid_in, std_in, 1, tm_in, ver_in);
    return i
};

exports.handler = (req, resp, context) => {

   try{
        var platform_in = req.queries["platform"]
        var vid_in = req.queries["vid"]
        var std_in = req.queries["sdt"]
        var tm_in = req.queries["tm"]
        var ver_in = req.queries["ver"]

        var oj = {"Status":"True", "VER":"CKEY7", "KEY":ckey7(platform_in, vid_in, std_in, "1", tm_in, ver_in)};
        resp.setHeader("Content-Type", "text/json");
        resp.send(JSON.stringify(oj));
        }catch(e){
            var oj = {"Status":"False", "Message": "未知错误，请参考错误信息，定位原因，或联系作者", "Info": e};
            resp.setHeader("Content-Type", "text/json");
            resp.send(JSON.stringify(oj));
          }
 
}