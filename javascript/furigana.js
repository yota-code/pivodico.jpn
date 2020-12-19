
var japanese_input = document.getElementById("japanese_input");
var furigana_input = document.getElementById("furigana_input");
var furigana_output = document.getElementById("furigana_output");
var japanese_output = document.getElementById("japanese_output");

var m = new ruby.Editor(furigana_input, furigana_output);
m.auto_refresh();

/* tab_select init */
var tab_header = document.getElementById("tab_header");

for (let e of document.getElementsByClassName("tab_select")) {
	tab_header.grow(
		"button", {'onclick' : "tab_select('" + e.id + "')"}
	).add_text(e.firstElementChild.textContent);
	e.onclick = tab_select(e.id);
}

/** ruby_select **/
/* init eventlistener */

document.getElementById("ruby_single_select").addEventListener("click", function(e) {
	if (e.target.nodeName == 'SPAN') {
		var kanji = e.target.parentNode.firstElementChild.textContent;
		var furigana = e.target.textContent;
		toggle_ruby_single(kanji, furigana, 'toggle');
	}
}, true);

document.getElementById("ruby_group_select").addEventListener("click", function(e) {
	if (e.target.nodeName == 'BUTTON') {
		activate_ruby_group(e.target.id);
	}
}, true);

function toggle_ruby_single(kanji, furigana, mode) {
	var n_div_s = document.getElementById("ruby_single_select");
	var n_div_r = document.getElementById("furigana_output");
	var s = document.getElementById("_s_{0}_{1}_".format(kanji, furigana));
	switch (mode) {
		case 'on' :
			s.classList.remove("_s_hidden");
			for (let r of n_div_r.getElementsByClassName('_r_{0}_{1}_'.format(kanji, furigana))) {
				r.style.display = "ruby-text";
			}
			break;
		case 'off' :
			s.classList.add("_s_hidden");
			for (let r of n_div_r.getElementsByClassName('_r_{0}_{1}_'.format(kanji, furigana))) {
				r.style.display = "none";
			}
			break;
		case 'toggle' :
			s.classList.toggle("_s_hidden");
			for (let r of n_div_r.getElementsByClassName('_r_{0}_{1}_'.format(kanji, furigana))) {
				r.style.display = s.classList.contains('_s_hidden') ? "none" : "ruby-text";
			}
			break;
	}
}

function activate_ruby_group(selector) {
	console.log('toggle_ruby_group('+selector+')');
	if (!(selector in learning_db || selector == '__none__' || selector == '__all__')) {
		return;
	}
	n_ul = document.getElementById("ruby_single_select");
	for (let kanji in m.furigana.occ) {
		for (let furigana in m.furigana.occ[kanji]) {
			if (kanji in ruby.furigana_db && furigana in ruby.furigana_db[kanji]) {
				var furigana_normal = (ruby.furigana_db[kanji][furigana] !== null) ? ruby.furigana_db[kanji][furigana] : furigana;
			}
			if ((selector == '__none__') ||	(
				learning_db.hasOwnProperty(selector) &&
				learning_db[selector].hasOwnProperty(kanji) &&
				learning_db[selector][kanji].hasOwnProperty(furigana_normal) &&
				learning_db[selector][kanji][furigana_normal] > 0
			)) {
				console.log("toggle_ruby_single", kanji, furigana);
				toggle_ruby_single(kanji, furigana, 'off');
			} else {
				toggle_ruby_single(kanji, furigana, 'on');
			}
		}
	}
}

/* refresh */
function grow_ruby_select() {
	n_div = document.getElementById("ruby_group_select").clear();
	n_div.grow("button", {'id' : '__none__'}).add_text('None');
	for (let k in learning_db) {
		n_div.grow("button", {'id' : k}).add_text(k);
	}
	n_div.grow("button", {'id' : '__all__'}).add_text('All');
	n_div = document.getElementById("ruby_single_select").clear();
	for (let kanji of Object.keys(m.furigana.occ).sort()) {
		n_li = n_div.grow('li');
		n_li.add_text('.').grow('strong').add_text(kanji);
		for (let furigana of Object.keys(m.furigana.occ[kanji]).sort()) {
			n_span = n_li.grow(
				'span',
				{'id': '_s_{0}_{1}_'.format(kanji, furigana)}
			).add_text(furigana);
		}
	}
}

function tab_select(tab_id) {
	for (let e of document.getElementsByClassName("tab_select")) {
		if (e.id == tab_id) {
			e.style.display = "block";
		} else {
			e.style.display = "none";
		}
	}
	switch (tab_id) {
		case 'step_two':
			mecab_process();
			grow_ruby_select();
			break;
		case 'settings':
			display_err();
			break;
	}
}

function display_err() {
	n_div = document.getElementById("settings_err").clear();
	for (let kanji in m.furigana.err) {
		for (let furigana of m.furigana.err[kanji]) {
			n_p = n_div.grow('p').add_text(kanji + '　');
			n_p.grow('input', {'type':'text', 'value':'｛' + furigana + '｝'});
		}
	}
}

function mecab_process() {
	var req = new XMLHttpRequest();
	req.open("POST", "/_mecab_process/", true);
	req.onload = function() {
		furigana_input.value = req.responseText;
		m.refresh();
	}
	req.setRequestHeader('Content-Type', 'text/plain');
	req.send(japanese_input.value);
}

m.refresh();

tab_select('step_two');

activate_ruby_group('__all__');
