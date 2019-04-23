// console.log("start");
/* FileSaver.js
 * A saveAs() FileSaver implementation.
 * 1.3.5
 * 2018-01-22 15:49:54
 *
 * By Eli Grey, https://eligrey.com
 * License: MIT
 *   See https://github.com/eligrey/FileSaver.js/blob/master/LICENSE.md
 */

/*global self */
/*jslint bitwise: true, indent: 4, laxbreak: true, laxcomma: true, smarttabs: true, plusplus: true */

/*! @source http://purl.eligrey.com/github/FileSaver.js/blob/master/src/FileSaver.js */

var saveAs = saveAs || (function(view) {
	"use strict";
	// IE <10 is explicitly unsupported
	if (typeof view === "undefined" || typeof navigator !== "undefined" && /MSIE [1-9]\./.test(navigator.userAgent)) {
		return;
	}
	var
		  doc = view.document
		  // only get URL when necessary in case Blob.js hasn't overridden it yet
		, get_URL = function() {
			return view.URL || view.webkitURL || view;
		}
		, save_link = doc.createElementNS("http://www.w3.org/1999/xhtml", "a")
		, can_use_save_link = "download" in save_link
		, click = function(node) {
			var event = new MouseEvent("click");
			node.dispatchEvent(event);
		}
		, is_safari = /constructor/i.test(view.HTMLElement) || view.safari
		, is_chrome_ios =/CriOS\/[\d]+/.test(navigator.userAgent)
		, throw_outside = function(ex) {
			(view.setImmediate || view.setTimeout)(function() {
				throw ex;
			}, 0);
		}
		, force_saveable_type = "application/octet-stream"
		// the Blob API is fundamentally broken as there is no "downloadfinished" event to subscribe to
		, arbitrary_revoke_timeout = 1000 * 40 // in ms
		, revoke = function(file) {
			var revoker = function() {
				if (typeof file === "string") { // file is an object URL
					get_URL().revokeObjectURL(file);
				} else { // file is a File
					file.remove();
				}
			};
			setTimeout(revoker, arbitrary_revoke_timeout);
		}
		, dispatch = function(filesaver, event_types, event) {
			event_types = [].concat(event_types);
			var i = event_types.length;
			while (i--) {
				var listener = filesaver["on" + event_types[i]];
				if (typeof listener === "function") {
					try {
						listener.call(filesaver, event || filesaver);
					} catch (ex) {
						throw_outside(ex);
					}
				}
			}
		}
		, auto_bom = function(blob) {
			// prepend BOM for UTF-8 XML and text/* types (including HTML)
			// note: your browser will automatically convert UTF-16 U+FEFF to EF BB BF
			if (/^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(blob.type)) {
				return new Blob([String.fromCharCode(0xFEFF), blob], {type: blob.type});
			}
			return blob;
		}
		, FileSaver = function(blob, name, no_auto_bom) {
			if (!no_auto_bom) {
				blob = auto_bom(blob);
			}
			// First try a.download, then web filesystem, then object URLs
			var
				  filesaver = this
				, type = blob.type
				, force = type === force_saveable_type
				, object_url
				, dispatch_all = function() {
					dispatch(filesaver, "writestart progress write writeend".split(" "));
				}
				// on any filesys errors revert to saving with object URLs
				, fs_error = function() {
					if ((is_chrome_ios || (force && is_safari)) && view.FileReader) {
						// Safari doesn't allow downloading of blob urls
						var reader = new FileReader();
						reader.onloadend = function() {
							var url = is_chrome_ios ? reader.result : reader.result.replace(/^data:[^;]*;/, 'data:attachment/file;');
							var popup = view.open(url, '_blank');
							if(!popup) view.location.href = url;
							url=undefined; // release reference before dispatching
							filesaver.readyState = filesaver.DONE;
							dispatch_all();
						};
						reader.readAsDataURL(blob);
						filesaver.readyState = filesaver.INIT;
						return;
					}
					// don't create more object URLs than needed
					if (!object_url) {
						object_url = get_URL().createObjectURL(blob);
					}
					if (force) {
						view.location.href = object_url;
					} else {
						var opened = view.open(object_url, "_blank");
						if (!opened) {
							// Apple does not allow window.open, see https://developer.apple.com/library/safari/documentation/Tools/Conceptual/SafariExtensionGuide/WorkingwithWindowsandTabs/WorkingwithWindowsandTabs.html
							view.location.href = object_url;
						}
					}
					filesaver.readyState = filesaver.DONE;
					dispatch_all();
					revoke(object_url);
				}
			;
			filesaver.readyState = filesaver.INIT;

			if (can_use_save_link) {
				object_url = get_URL().createObjectURL(blob);
				setTimeout(function() {
					save_link.href = object_url;
					save_link.download = name;
					click(save_link);
					dispatch_all();
					revoke(object_url);
					filesaver.readyState = filesaver.DONE;
				});
				return;
			}

			fs_error();
		}
		, FS_proto = FileSaver.prototype
		, saveAs = function(blob, name, no_auto_bom) {
			return new FileSaver(blob, name || blob.name || "download", no_auto_bom);
		}
	;
	// IE 10+ (native saveAs)
	if (typeof navigator !== "undefined" && navigator.msSaveOrOpenBlob) {
		return function(blob, name, no_auto_bom) {
			name = name || blob.name || "download";

			if (!no_auto_bom) {
				blob = auto_bom(blob);
			}
			return navigator.msSaveOrOpenBlob(blob, name);
		};
	}

	FS_proto.abort = function(){};
	FS_proto.readyState = FS_proto.INIT = 0;
	FS_proto.WRITING = 1;
	FS_proto.DONE = 2;

	FS_proto.error =
	FS_proto.onwritestart =
	FS_proto.onprogress =
	FS_proto.onwrite =
	FS_proto.onabort =
	FS_proto.onerror =
	FS_proto.onwriteend =
		null;

	return saveAs;
}(
	   typeof self !== "undefined" && self
	|| typeof window !== "undefined" && window
	|| this
));

var search =  function (nc, mn) {
  console.log("准备爬取");
  setTimeout(function () {

      if (document.title == "商标网上检索系统") {
          console.log(document.title + "=商标网上检索系统");
          document.getElementsByTagName('table')[0].click();
      }
      else if (document.title == "商标近似检索") {
      		var x = window.innerWidth / 2.0, y = window.innerHeight / 2.0;
      		for (var i = 0;i < 50;i++) {
      			var e = document.createEvent("MouseEvents");
      			e.initMouseEvent("mousemove", true, true, window, 1, x + 1, y + 1, x + 1, y + 1, false, false, false, false, 0, null);
      			document.dispatchEvent(e);
					}
          console.log(document.title + "=商标近似检索");
          document.getElementById("nc").value = nc;
          document.getElementById("nc").focus();
          document.getElementById("nc").click();
          document.getElementById("mn").value = mn;
          document.getElementById("mn").focus();
          document.getElementById("mn").click();
          // document.getElementById("nc").click();
          // console.log("添加新的按钮");
          // var MyDiv =document.getElementById("cntvlive2-is-installed");
          // var bt =document.createElement("button");           //createElement生成button对象
          // bt.innerHTML = '删除';
          // bt.id = "new_button";
          // bt.onclick = function (ev) {
          // document.getElementById("nc").focus();
          //   document.getElementById("_searchButton").click();
          // };
          // MyDiv.appendChild(bt);
          // console.log("准备点击新按钮");
          // document.getElementById("new_button").click();
          // console.log("已经点击新按钮");
          // document.getElementById("submitForm").submit();
          console.log("准备点击查询");
          setTimeout(function () {
            document.getElementById("_searchButton").focus();
            document.getElementById("_searchButton").click();
            console.log("已经点击查询");
          }, 100);
      }
      else if (document.title == "商标检索结果") {
          console.log("开始爬取");
          setTimeout(function () {
              var res = [];
              var a = document.getElementsByTagName('tr');
              for (var key in a) {
                if (a[key].className == "ng-scope") {
                  var b = a[key].children, r=[];
                  for (var k in b) {
                    if(b[k].innerText != undefined && b[k].innerText != "") {
                      r.push(b[k].innerText);
                    }
                  }
                  res.push(r.join('\t'));
                }
              }
              var text = res.join('\n');
              var filename = 'crawler_result_国际分类=' + nc + '_商标名称=' + mn + '.txt';
              var blob = new Blob([text], {type: "text/plain;charset=utf-8"});
              saveAs(blob, filename);
              console.log("爬取结束，共" + res.length+ "条商标数据。");
          }, 5000);

      }
    }
  , 5000);
};

search(9, "手机");

