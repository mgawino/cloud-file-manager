jQuery.each(["post", "put", "delete"], function( i, method ) {
  jQuery[method] = function( url, data, callback, type ) {
    if (jQuery.isFunction(data)) {
      type = type || callback;
      callback = data;
      data = undefined;
    }

    return jQuery.ajax({
      url: url,
      type: method,
      dataType: type,
      contentType: "application/json",
      data: JSON.stringify(data),
      success: callback
    });
  };
});

function create_node() {
    var tree = $('#tree').jstree(true);
    var selected = tree.get_selected();
    if(!selected.length) {
        selected = tree.create_node(null, {"type":"bucket"});
    } else {
        selected = selected[0];
        selected = tree.create_node(selected, {"type":"folder"});
    }
    tree.edit(selected);
};

function rename_node() {
    var tree = $('#tree').jstree(true);
    var selected = tree.get_selected();
    if(!selected.length) {
        return false;
    };
    selected = selected[0];
    tree.edit(selected);
}

function on_rename_node(data) {
    var tree = $('#tree').jstree(true);
    var node = data.node;
    if (data.old === "New node") {
        var create_data = {
            path: tree.get_path(node, '/', false)
        };
        $.post('/node', create_data, function(data) {
            console.log('Created node');
        }).fail(function() {
            console.log('Create node failed');
            tree.delete_node(node);
        });
    } else {
        console.log(data);
        if (data.node.parent == '#') {
            var old_path = data.old;
        } else {
            var parent = tree.get_node(data.node.parent);
            var old_path = tree.get_path(parent) + '/' + data.old
        }
        var rename_data = {
            old_path: old_path,
            new_path: tree.get_path(node, '/', false)
        }
        $.put('/node', rename_data, function(data) {
            console.log('Renamed node');
        }).fail(function() {
            console.log('Rename node failed');
        });
    }

};

function delete_node() {
    var tree = $('#tree').jstree(true);
    var selected = tree.get_selected();
    if(!selected.length) {
        return false;
    }
    selected = selected[0];
    var delete_data = {
        path: tree.get_path(selected, '/', false)
    }
    $.delete('/node', delete_data, function(data) {
        console.log('Deleted node');
        tree.delete_node(selected);
    }).fail(function() {
        console.log('Delete node failed');
    });
};

$(document).ready(function(){
    $('#tree').on('rename_node.jstree', function(event, data) {
        on_rename_node(data);
    }).jstree({
      "core": {
        "animation": 0,
        "check_callback": true,
        "data" : {"url": "/tree"}
      },
      "types" : {
        "bucket": {
          "icon": "/static/icons/bucket",
          "valid_children": ["folder"]
        },
        "folder": {
          "valid_children": ["folder"]
        }
      },
      "plugins" : ["state", "types"]
    });
})
