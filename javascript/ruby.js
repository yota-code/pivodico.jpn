
function isinstance(obj, typ) {
	return (Object.prototype.toString.call(obj) === '[object ' + typ + ']');
}

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

var ruby = {
	normalize: function(s) {
		return s;
	},

	//rec: /((（[\u3041-\u3096\u30A1-\u30F6]+）)|(｛([^｛｜｝]+)｜([^｛｜｝]+)｝))/g,

	rec: /((（([^（）]+)）)|(｛([^｛｜｝]+)｜([^｛｜｝]+)｝))/g,

	furigana_db: furigana_db,

	jukujikun_db: jukujikun_db,

	Duplex: class {

		constructor(kanji, furigana, is_implicit) {
			this._k_original = kanji;
			this._f_original = furigana;
			this._k_normal = ruby.normalize(kanji);
			this._f_normal = ruby.normalize(furigana);
			this.is_implicit = (is_implicit) ? true : false;
		}

		seek(i, j) {
			return [
				(i === null || i === undefined) ? (this._k_original.length) : (i),
				(j === null || j === undefined) ? (this._f_original.length) : (j)
			];
		}

		k_original(right, size) {
			var left = right - size;
			return [this._k_original.substring(left, right), left];
		}

		k_normal(right, size) {
			var left = right - size;
			return [this._k_normal.substring(left, right), left];
		}

		f_original(right, size) {
			var left = right - size;
			return [this._f_original.substring(left, right), left];
		}

		f_normal(right, size) {
			var left = right - size;
			return [this._f_normal.substring(left, right), left];
		}

		original(k_right, f_right, k_size, f_size) {
			var [k, k_left] = this.k_original(k_right, k_size);
			var [f, f_left] = this.f_original(f_right, f_size);
			return [k, f, k_left, f_left];
		}

		normal(k_right, f_right, k_size, f_size) {
			var [k, k_left] = this.k_normal(k_right, k_size);
			var [f, f_left] = this.f_normal(f_right, f_size);
			return [k, f, k_left, f_left];
		}

	},
	
	Converter: class {
		constructor() {
			this.furigana = new ruby.Furigana(false);
		}
		
		escape_special(txt) {
			txt = txt.replaceAll('\\｛', '__obrace__');
			txt = txt.replaceAll('\\（', '__oparen__');
			return txt;
		}

		restore_special(txt) {
			txt = txt.replaceAll('__obrace__', '｛');
			txt = txt.replaceAll('__oparen__', '（');
			return txt;
		}
		
		to_html5(txt) {
			txt = this.escape_special(txt);
			var stack = new Array();
			var prev = 0;
			var k_part, f_part;
			var is_implicit;
			var res = ruby.rec.exec(txt)
			while (res !== null) {
				if (( res[5] !== undefined ) && ( res[6] !== undefined )) {
					is_implicit = false;
					k_part = res[5];
					f_part = res[6];
					stack.push(txt.slice(prev, res.index));
				} else if ( res[3] !== undefined ) {
					let start = Math.max(prev, 0, res.index - res[3].length);
					is_implicit = true;
					k_part = txt.slice(start, res.index);
					f_part = res[3];
					stack.push(txt.slice(prev, start));
				}
				stack.push(this.furigana.to_html5(k_part, f_part, is_implicit));
				prev = ruby.rec.lastIndex;
				res = ruby.rec.exec(txt)
			}
			stack.push(txt.slice(prev));
			return this.restore_special(stack.join(''));
		}
	
	},

	Editor: class {
		constructor(n_input, n_output) {
			this.furigana = new ruby.Furigana(false);

			this.n_input = n_input;
			this.n_output = n_output;

			this.prev_time = 0.0;
			this.prev_text = "";
			//this.to_be_refreshed = true;

			// n_input.keyup = function() {
			// 	console.log("KEYUP");
			// 	this.to_be_refreshed = true;
			// };
		}

		/*_prepare_ruby_visibility() {

			prepare an object which contains the state of the displayed ruby ?

			this.ruby_map = new Object();
			for (let kanji in this.furigana.occ) {
				if (!(kanji in this.ruby_map)) {
					this.ruby_map[kanji] = new Object();
				}
				for (let furigana in this.furigana.occ[kanji]) {
					this.ruby_map[kanji][furigana] = true;
				}
			}
		}*/



		refresh() {
			console.log("refresh");
			this.n_output.innerHTML = this.to_html5(this.n_input.value);
		}

		auto_refresh() {
			var curr_time = Date.now();


			var other = this;
			if ((curr_time - this.prev_time) > 2500.0) {
				if (this.n_input.value != this.prev_text) {
					this.prev_text = this.n_input.value;
					this.refresh();
				}
				this.prev_time = curr_time;
			}

			window.requestAnimationFrame(function() {
				other.auto_refresh();
			});

			return this;
		}


	},

	Furigana: class {
		constructor(grouped) {
			this.grouped = grouped;

			this.j_max = new Map();
			for (let k in ruby.furigana_db) {
				this.j_max.set(
					k,
					Math.max( ... Array.from(Object.keys(ruby.furigana_db[k]), o => o.length))
				);
			}

			this.occ = new Object(); // store the reading occurences
			this.err = new Object();
		}

		* match_kanji(w, i, j) {
			[i, j] = w.seek(i, j);
			var [k, p] = w.k_normal(i, 1);
			if (k in ruby.furigana_db) {
				var j_lim = Math.min(j, this.j_max.get(k));
				for (let z=1 ; z <= j_lim ; z++) {
					var [f, q] = w.f_normal(j, z);
					if (f in ruby.furigana_db[k]) {
						yield w.original(i, j, 1, z);
					}
				}
			}
		}

		* match_jukujikun(w, i, j) {
			[i, j] = w.seek(i, j);
			var m = ruby.jukujikun_db;
			var [k, p] = w.k_normal(i, 1);
			while (k in m) {
				m = m[k];
				for (let a in m) {
					var b = m[a];
					if ( b === null ) {
						var [f, q] = w.f_normal(j, a.length);
						if (a == f) {
							yield w.original(i, j, i - p, a.length);
						}
					}
				}
				[k, p] = w.k_normal(p, 1);
			}
		}

		match_kana(w, i, j) { // to be retrofitted
			[i, j] = w.seek(i, j);
			var z = 1;
			var [k, p] = w.k_normal(i, z);
			var [f, q] = w.f_normal(j, z);
			while (k == f) {
				z += 1;
				if (p <= 0 || q <= 0) {
					break;
				}
				[k, p] = w.k_normal(i, z);
				[f, q] = w.f_normal(j, z);
			}
			return (z > 1) ? w.original(i, j, z-1, z-1) : null;
		}

		* match(w, i, j) {
			[i, j] = w.seek(i, j);
			var [k, p] = w.k_normal(i, 1);
			if (k in ruby.jukujikun_db) {
				yield * this.match_jukujikun(w, i, j);
			}
			if (k in ruby.furigana_db) {
				yield * this.match_kanji(w, i, j);
			} else {
				var ret = this.match_kana(w, i, j);
				if ( ret !== null ) {
					yield ret;
				}
			}
		}

		split(w, i, j, stack, depth) {
			if (stack === undefined) {
				stack = new Array();
			}
			if (depth === undefined) {
				depth = 0;
			}
			[i, j] = w.seek(i, j);
			if (i <= 0) {
				if (j <= 0) {
					return stack;
				} else {
					return null;
				}
			}
			if (j <= 0) {
				if (w.is_implicit) {
					if (i <= 0) {
						return stack
					} else {
						console.log("warning, implicit padding");
						var [k, p] = w.k_original(i, i);
						return [k,].concat(stack);
					}
				} else {
					if (i <= 0) {
						return stack;
					} else {
						return null;
					}
				}
			}
			for (var [k, f, p, q] of this.match(w, i, j)) {
				var v = this.split(w, p, q, [[k, f],].concat(stack), depth+1);
				if (v !== null) {
					return v;
				}
			}
		}

		push_occ(kanji, furigana) {
			/* each time a reading is seen, add it to the occurence counter */
			if (!(kanji in this.occ)) {
				this.occ[kanji] = new Object();
			}
			var line = this.occ[kanji];
			if (!(furigana in line)) {
				line[furigana] = 0;
			}
			line[furigana] += 1;
		}

		push_err(kanji, furigana) {
			if (!(kanji in this.err)) {
				this.err[kanji] = new Array();
			}
			var line = this.err[kanji];
			if (!(furigana in line)) {
				line.push(furigana);
			}
		}

		join(stack) {
			var result = new String();
			if (this.grouped) {
				var rb = new Array();
				var rt = new Array();
				for (let v of stack) {
					if (isinstance(v, "String")) {
						result += v;
					} else {
						if (v[0] != v[1]) {
							this.push_occ(v[0], v[1]);
						}
						rb.push(v[0]);
						rt.push(v[1]);
					}
				}
				result += '<ruby>' + rb.join('<rb>') + '<rt>' + rt.join('<rt>') + '</ruby>';
			} else {
				for (let v of stack) {
					if (isinstance(v, "String")) {
						result += v;
					} else {
						if (v[0] == v[1]) {
							result += v[0];
						} else {
							this.push_occ(... v);
							result += '<ruby>{0}<rt class="_r_{0}_{1}_">{1}</ruby>'.format(... v);
						}
					}
				}
			}
			return result;
		}

		to_html5(kanji, furigana, is_implicit) {
			var u = new ruby.Duplex(kanji, furigana, is_implicit);
			var stack = this.split(u);
			if (stack) {
				return this.join(stack);
			} else {
				this.push_err(kanji, furigana);
				return '<ruby>{0}<rt>{1}</ruby>'.format(kanji, furigana);
			}
		}
	}
};
