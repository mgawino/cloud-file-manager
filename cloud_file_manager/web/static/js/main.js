function create_node() {
    var tree = $('#tree').jstree(true);
    var sel = tree.get_selected();
    if(!sel.length) {
        return false;
    }
    sel = sel[0];
    sel = tree.create_node(sel, {"type":"folder"});
    if(sel) {
        tree.edit(sel);
    }
};

function rename_node() {
    var tree = $('#tree').jstree(true);
    var sel = tree.get_selected();
    if(!sel.length) {
        return false;
    }
    sel = sel[0]
    tree.edit(sel);
};

function delete_node() {
    var tree = $('#tree').jstree(true);
    var sel = tree.get_selected();
    if(!sel.length) {
        return false;
    }
    tree.delete_node(sel);
};

$(document).ready(function(){
    $('#tree').on('create_node.jstree', function(event, data) {
        console.log('create node');
    }).on('rename_node.jstree', function(event, data) {
        console.log('rename node');
    }).on('delete_node.jstree', function(event, data) {
        console.log('delete node');
    }).jstree({
      "core" : {
        "animation" : 0,
        "check_callback" : true,
        "themes" : { "stripes" : true },
        "data" : {
            "url": "/tree"
        }
      },
      "types" : {
        "bucket" : {
          "icon" : "/static/icons/bucket",
          "valid_children" : ["folder", "file"]
        },
        "file" : {
          "icon" : "glyphicon glyphicon-file",
          "valid_children" : []
        }
      },
      "plugins" : [
        "contextmenu", "dnd", "search", "state", "types", "wholerow"
      ]
    });
})
