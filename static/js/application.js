// Globals
var g_app_name = 'jabjot';
var g_section = '';
var g_last_note_kind = '';
var g_note_index = 0;
var g_note_index_cookie = g_app_name + '_g_note_index';
var g_note_max_index = 0;
var g_last_url_cookie = g_app_name + '_last_url';
var g_page = 1;
var g_has_next_page = false;
var g_interval_flash = 0;

// Document ready (on load)
function documentReady() {
  fixPngs();
	//tableColors();
	//textClasses();
	dropdowns();
	btnMenus();
}

// Create cookie
function createCookie(name, value, days) {
  var date = new Date();
  date.setTime(date.getTime()+(days*24*60*60*1000));
  var expires = "; expires="+date.toGMTString();
  document.cookie = name+"="+value+expires+"; path=/";
}

// Read cookie
function readCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i=0;i < ca.length;i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1,c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
  }
  return null;
}

// Delete cookie
function deleteCookie(name) {
  createCookie(name,"",-1);
}

// Scroll
$.fn.scrollView = function () {
  return this.each(function () {
    $('html, body').animate({
        scrollTop: $(this).offset().top
      }, 50);
  });
}

// Button menus
function btnMenus() {
  $(".btn_menus").each(function() {
    var id = $(this).attr("id");
		var part = id.split("_");
		part = part[1];

		var id_menu = "menu_" + part;

		var offset = $(this).offset();
		var width = $('#' + id_menu).css('width').split('px');
		width = width[0];

		$("#" + id_menu).css({"left": (offset.left - width / 3) + "px", "top": (offset.top + 15) + "px"});

		$(this).mouseover(function() {
			$("#" + id_menu).css("display", "block");
		});

		$("#" + id_menu).mouseover(function() {
			$("#" + id_menu).css("display", "block");
		});

		$(this).mouseout(function() {
			$("#" + id_menu).css("display", "none");
		});

		$("#" + id_menu).mouseout(function() {
			$("#" + id_menu).css("display", "none");
		});

		if(!$(this).is('.click_trough')) {
			$(this).click(function(event) {
			  event.preventDefault();
		  });
		}
  });
}

// Dropdowns
function dropdowns() {
  $(".dropdown").each(function() {
    var id = $(this).attr("id");
		var part = id.split("_");
		part = part[1];

		var id_menu = "menu_" + part;

		var offset = $(this).offset();

		$("#" + id_menu).css({"left": (offset.left - 20) + "px", "top": (offset.top + 12) + "px"});

		$(this).click(function() {
		  return false;
	  });

		$(this).mouseover(function() {
			$("#" + id_menu).css("display", "block");
		});

		$("#" + id_menu).mouseover(function() {
			$("#" + id_menu).css("display", "block");
		});

		$(this).mouseout(function() {
			$("#" + id_menu).css("display", "none");
		});

		$("#" + id_menu).mouseout(function() {
			$("#" + id_menu).css("display", "none");
		});
  });
}

// Is Numeric support
function isNumeric(input) {
    return (input - 0) == input && input.length > 0;
}

// Shows loading box
function showLoading() {
	$('#loading').centerInClient();
	$('#loading').css("display", "block");
}

// Hides loading box
function hideLoading() {
	$("#loading").fadeOut("fast");
}

// Shows or hides a div
function toggle(id) {
  if($("#" + id).css("display") == "none") {
    $("#" + id).css("display", "block");
  } else {
    $("#" + id).css("display", "none");
  }
}

// Arregla PNGs para IE6
function fixPngs() {
	$('body').supersleight();
}

// Alterna colores de rows de una tabla
function tableColors() {
	$("tr:even").css("background-color", "#dddddd");
	$("tr:odd").css("background-color", "#ffffff");
	$("table.portada tr").css("background-color", "#ffffff");

	$("tr:even").mouseover(function() {
		$(this).css("background-color", "yellow");
	});

	$("tr:even").mouseout(function() {
		$(this).css("background-color", "#dddddd");
	});

	$("tr:odd").mouseover(function() {
		$(this).css("background-color", "yellow");
	});

	$("tr:odd").mouseout(function() {
		$(this).css("background-color", "#ffffff");
	});
}

// Agrega clase de text a todos los textfields
function textClasses() {
  $('input[type=submit]').addClass('button');
  $('input[type=button]').addClass('button');

	$('input[type=text]').addClass('text');
	$('input[type=password]').addClass('text');

  $('.small input[type=text]').addClass('small');
  $('.small select').addClass('small');
  $('.small input[type=submit]').addClass('small');
  $('.small input[type=button]').addClass('small');
}

// Shows the remote window
function showRemote() {
  $("#remote").centerInClient();
  $("#remote").css("display", "block");
  documentReady();
}

// Hides the remote window
function hideRemote() {
  $("#remote").css("display", "none");
}

// Displays html in remote window
function displayRemote(html) {
  html = '<div class="fright"><a href="#" onclick="hideRemote(); return false;">X</a></div>' + html + '<div class="break"><!-- i --></div>';
  $("#remote").html(html);
}

// Checks key shortcuts
function checkKeys(event) {
  if(event.which && (event.which == 191 || event.which == 188)) {
    // Slash key
    focusShortcuts();
  } else if(event.which && event.which == 27) {
    // ESC key
    unfocusShortcuts();
  } else if(event.which && event.which == 190) {
    // . Key
    focusTitle();
  } else if(g_section == 'notes_email') {
    // U key, go back
    if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
      returnToIndex();
    }
  } else if(g_section == 'notes_index') {
    // Specific bindings for notes index
    if(event.which && event.which == 76) {
      // L, next page
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        goNextPage();
      }
    } else if(event.which && event.which == 72) {
      // H, prev page
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        goPrevPage();
      }
    } else if(event.which && event.which == 74) {
      // J, down
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        if(g_note_index < g_note_max_index) {
          g_note_index++;
          focusNote(g_note_index, true);
        }
      }
    } else if(event.which && event.which == 75) {
      // K, up
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        if(g_note_index > 1) {
          g_note_index--;
          focusNote(g_note_index, true);
        }
      }
    } else if(event.which && event.which == 88) {
      // x key, view note
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        goToNote(g_note_index);
      }
    } else if(event.which && event.which == 69) {
      // E key, edit
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        editNote(g_note_index);
      }
    } else if(event.which && event.which == 68) {
      // D key, delete
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        delNote(g_note_index);
      }
    } else if(event.which && event.which == 86) {
      // V key, view url if possible
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        viewNote(g_note_index);
      }
    } else if(event.which && event.which == 85) {
      // U key, go back
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        returnToIndex();
      }
    } else if(event.which && event.which == 77) {
      // M key, email note
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        emailNote(g_note_index);
      }
    }
  } else if(g_section == 'notes_view') {
    if(event.which && event.which == 74) {
      // J, next
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        goNextNote();
      }
    } else if(event.which && event.which == 75) {
      // K, prev
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        goPrevNote();
      }
    } else if(event.which && event.which == 82) {
      // R key, view raw
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        toggleRaw();
      }
    } else if(event.which && event.which == 83) {
      // S key, view scrape
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        toggleScrape();
      }
    } else if(event.which && event.which == 77) {
      // M key, email note
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        emailNoteObjectId($("#note_object_id").html());
      }
    } else if(event.which && event.which == 85) {
      // U key, go back
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        returnToIndex();
      }
    } else if(event.which && event.which == 69) {
      // E key, edit
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        editNoteObjectId($("#note_object_id").html());
      }
    } else if(event.which && event.which == 68) {
      // D key, delete
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        delNoteObjectId($("#note_object_id").html());
      }
    } else if(event.which && event.which == 86) {
      // V key, view url if possible
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        if($("#note_kind").html() == 'todo') {
          var id = $("#note_object_id").html();
          var checkbox_id = "todo_done_" + id;

          if($("#" + checkbox_id).is(":checked")) {
            $("#" + checkbox_id).attr('checked', false);
          } else {
            $("#" + checkbox_id).attr('checked', true);
          }

          toggleNoteDone(id);
        } else if($("#note_kind").html() == 'bookmark') {
          openNoteUrl();
        }
      }
    }
  } else if(g_section == 'notes_edit' || g_section == 'notes_new') {
    if(event.which && event.which == 85) {
      // U key, go back
      if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
        returnToIndex();
      }
    }
  }
}

// Set current page
function setPage(page) {
  g_page = page;
}

// Set next page
function setHasNextPage(has_next_page) {
  g_has_next_page = has_next_page;
}

// Go to the next page
function goNextPage() {
  if(g_has_next_page) {
    g_page++;

    if(getUrlQueryString(true)) {
      var url = '/notes?' + getUrlQueryString(true);

      url = url.replace(new RegExp("\\?p=[0-9]+", "gi"), '?');
      url = url.replace(new RegExp("\\&p=[0-9]+", "gi"), '');
      url = url.replace('?&', '?');
      url += '&';
    } else {
      url = '/notes?';
    }

    url += 'p=' + g_page;

    g_note_index = 1;
    createCookie(g_note_index_cookie, g_note_index, 30);

    location.href = url;
  }
}

// Go to the prev page
function goPrevPage() {
  if(g_page > 1) {
    g_page--;

    if(getUrlQueryString(true)) {
      var url = '/notes?' + getUrlQueryString(true);

      url = url.replace(new RegExp("\\?p=[0-9]+", "gi"), '?');
      url = url.replace(new RegExp("\\&p=[0-9]+", "gi"), '');
      url = url.replace('?&', '?');
      url += '&';
    } else {
      url = '/notes?';
    }

    url += 'p=' + g_page;

    g_note_index = 1;
    createCookie(g_note_index_cookie, g_note_index, 30);

    location.href = url;
  }
}

// Return to note's index (last index url)
function returnToIndex() {
  var last_url = readCookie(g_last_url_cookie);

  if(last_url) {
    location.href = last_url;
  } else {
    location.href = '/notes';
  }
}

// View note (open url by index)
function viewNote(index) {
  if(getNoteKind(index) == 'bookmark') {
    var url = getNoteUrl(index);
    if(url != "") {
      window.open(url, '_blank');
    }
  } else if(getNoteKind(index) == 'todo') {
    var id = getNoteObjectId(index);
    var checkbox_id = "todo_done_" + id;

    if($("#" + checkbox_id).is(":checked")) {
      $("#" + checkbox_id).attr('checked', false);
    } else {
      $("#" + checkbox_id).attr('checked', true);
    }

    toggleNoteDone(id);
  }
}

// Open note url
function openNoteUrl() {
  var kind = $("#note_kind").html();
  if(kind == 'bookmark') {
    var url = $("#note_url").html();
    window.open(url, '_blank');
  }
}

// Edit note via object id
function editNoteObjectId(oid) {
  var is_owned = $("#is_owned").html();

  if(is_owned == "1") {
    location.href = '/notes/edit/' + oid;
  } else {
    flash("You don't own this note.", 'error');
  }
}

// Delete note via object id
function delNoteObjectId(oid) {
  var is_owned = $("#is_owned").html();

  if(is_owned == "1") {
    var conf = confirm('are you sure?');

    if(conf) {
      location.href = '/notes/del/' + oid;
    }
  } else {
    flash("You don't own this note.", 'error');
  }
}

// Get note object id
function getNoteObjectId(index) {
  var object_id = $("#note_" + index).children('.item_object_id')[0].innerHTML;

  return object_id;
}

// Get note kind
function getNoteKind(index) {
  var kind = $("#note_" + index).children('.item_kind')[0].innerHTML;

  return kind;
}

// Get note url
function getNoteUrl(index) {
  var url = $("#note_" + index).children('.item_url')[0].innerHTML;

  return url;
}

// Delete note
function delNote(index) {
  var conf = confirm('are you sure?');

  if(conf) {
    location.href = '/notes/del/' + getNoteObjectId(index);
  }
}

// Edit note
function editNote(index) {
  location.href = '/notes/edit/' + getNoteObjectId(index);
}

// Go to a Note
function goToNote(index) {
  location.href = '/notes/' + getNoteObjectId(index);
}

// Itirate and number notes
function itirateNotes() {
  var count = 1;

  $(".note").each(function() {
    $(this).attr('id', 'note_' + count);
    g_note_max_index = count;
    count++;
  });
}

// Focus note
function focusNote(index, scroll) {
  if(index > 0 && index <= g_note_max_index) {
    $(".note").each(function() {
      $(this).removeClass("focused");
    });

    $("#note_" + index).addClass("focused");

    if(scroll) {
      // Check if we gotta scroll
      var w_top = $(window).scrollTop();
      var w_bottom = $(window).height() + $(window).scrollTop();
      var offset = $("#note_" + index).offset();

      if(offset.top < w_top || offset.top + 50 > w_bottom) {
        $("#note_" + index).scrollView();
      }
    }

    createCookie(g_note_index_cookie, g_note_index, 30);
  }
}

// Check if we gotta prefocus a note?
function preFocusNote() {
  var index_cookie = readCookie(g_note_index_cookie);

  if(index_cookie) {
    if(index_cookie == 0) {
      index_cookie = 1;
    }
    setNoteIndex(index_cookie / 1);
    focusNote(g_note_index);
    return true;
  }
}

// Sets note index
function setNoteIndex(index) {
  if(index > 0 && index <= g_note_max_index) {
    g_note_index = index;
  }
}

// Focus on note title form
function focusTitle() {
  if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
    $("#note_title").focus();
    $("#note_title").select();
  }
}

// Focus on shortcuts textfield
function focusShortcuts() {
  if(!$("#sc").is(':focus') && !$(".form_field").is(':focus')) {
    $("#sc").select();
    $("#sc").focus();
    $("#header").scrollView();
  }
}

// Remove focus from shortcuts
function unfocusShortcuts() {
  $("#sc").blur();
  $(".form_field").blur();
  $("#raw").css('display', 'none');
}

// Go Shortcut Go!
function goShortcut() {
  var sc = $("#sc").val();

  if(sc == "nn") {
    // New Note
    location.href = '/notes/new';
  } else if(sc == "nb") {
    // New Bookmark
    location.href = '/notes/new?bookmark=1';
  } else if(sc == "nt") {
    // New TO-DO
    location.href = '/notes/new?todo=1';
  } else if(sc == 'n') {
    // Notes
    location.href = '/notes';
  } else if(sc.match(new RegExp("^\\s?p:\\s?[0-9]+\\s?$", "gi"), '?')) {
    var page = sc.split('p:');

    if(page.length > 0) {
      var page = page[1].trim();

      location.href = '/notes?p=' + page;
    }
  } else if(sc != '') {
    // Default, run search
    location.href = '/notes?q=' + sc;
  } else {
    // Empty default, go to notes
    location.href = '/notes';
  }
}

// Checks note kind
function checkKind() {
  var kind = $("#note_kind").val();

  if(kind == 'todo') {
    $("#cont_url").css('display', 'none');
    $("#cont_done").css('display', 'block');
    g_last_note_kind = kind;
  } else if(kind == 'bookmark') {
    $("#cont_url").css('display', 'block');
    $("#cont_done").css('display', 'none');
    g_last_note_kind = kind;
  } else if(g_last_note_kind != kind) {
    $("#cont_url").css('display', 'none');
    $("#cont_done").css('display', 'none');
    g_last_note_kind = kind;
  }
}

// Gets current url
function getUrl(current) {
  if(current) {
    return document.location.href;
  } else {
    return readCookie(g_last_url_cookie);
  }
}

// Gets current url's query string
function getUrlQueryString(current) {
  var url = getUrl(current);
  var parts = url.split('?');

  if(parts.length > 0) {
    return parts[1];
  } else {
    return false;
  }
}

// Sets section
function setSection(section) {
  g_section = section;

  if(section == 'notes_index') {
    var q = getUrlQueryString(true);

    if(q) {
      createCookie(g_last_url_cookie, '/notes?' + q, 30);
    } else {
      createCookie(g_last_url_cookie, '/notes', 30);
    }
  }
}

// Toggle done on a todo
function toggleNoteDone(id) {
  var checkbox_id = "todo_done_" + id;
  var done = 0;

  if($("#" + checkbox_id).is(":checked")) {
    done = 1;
  }

  $.ajax({
    url: "/notes/toggle_done?id=" + id + "&done=" + done,
    success: function(data) {
      if(data == 'err_not_found') {
        flash('The note does not exist!', 'error');
      } else if(data == 'err_logged') {
        flash("You must login to do this.", "error");
      } else if(data == 'err_owner') {
        flash("You're not the owner of this note.", "error");
      }
    }
  });
}

// Toggle raw view
function toggleRaw() {
  if($("#raw").css('display') == 'none') {
    $("#raw").css('display', 'block');
    $("#raw textarea").select();
    $("#raw").scrollView();
  } else {
    $("#raw").css('display', 'none');
  }
}

// Toggle scrape view
function toggleScrape() {
  if($("#scrape").css('display') == 'none') {
    $("#scrape").css('display', 'block');

    if($("#scrape_content").html() == '<!-- i -->') {
      $("#scrape_content").html('Loading...');

      $.ajax({
        url: "/notes/get_scrape/" + $("#note_object_id").html(),
        success: function(data) {
          if(data == 'err_not_found') {
            flash('The note does not exist!', 'error');
          } else if(data == 'err_login') {
            flash('You must login to do that!', 'error');
          } else if(data == 'err_owner') {
            flash("You're not the owner of this note!", "error");
          } else {
            $("#scrape_content").html(data);
            $("#scrape").scrollView();
          }
        }
      });
    } else {
      $("#scrape").scrollView();
    }
  } else {
    $("#scrape").css('display', 'none');
  }
}

// Go next note
function goNextNote() {
  var next_note = $("#next_note").html();
  var index_cookie = readCookie(g_note_index_cookie);

  if(next_note != "" && index_cookie < 20) {
    index_cookie++;
    createCookie(g_note_index_cookie, index_cookie, 30);
    location.href = '/notes/' + next_note;
  } else if(index_cookie == 20) {
    flash('End of page', 'error');
  }
}

// Go prev note
function goPrevNote() {
  var prev_note = $("#prev_note").html();
  var index_cookie = readCookie(g_note_index_cookie);

  if(prev_note != "" && index_cookie > 1) {
    index_cookie--;
    createCookie(g_note_index_cookie, index_cookie, 30);
    location.href = '/notes/' + prev_note;
  } else if(index_cookie == 1) {
    flash('Top of page', 'error');
  }
}

// Send note via email and index
function emailNote(index) {
  location.href = '/notes/email/' + getNoteObjectId(index);
}

// Send note via email and object id
function emailNoteObjectId(id) {
  location.href = '/notes/email/' + id;
}

// Flashes message
function flash(msg, type) {
  clearInterval(g_interval_flash);
  $("#msg").html(msg);
  $("#msg").centerInClient();
  if(type == "error") {
    $("#msg").addClass('msg_error');
  } else {
    $("#msg").addClass('msg_notice');
  }
  $("#msg").css('display', 'block');

  g_interval_flash = setInterval(function() {
    hideFlash();
  }, 3000);
}

// Hide flash message
function hideFlash() {
  clearInterval(g_interval_flash);
  $("#msg").css('display', 'none');
}

// On ready
$(document).ready(function() {
  documentReady();

  setTimeout(function() {
    $(document).bind('keyup', checkKeys);
  }, 250);

  $("#loading")
    .hide()
    .ajaxStart(function() {
      //showLoading();
    })
    .ajaxStop(function() {
      //hideLoading();
    })
  ;
});
