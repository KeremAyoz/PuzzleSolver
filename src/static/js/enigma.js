var board;
var sol_board;
//listeners
$(function() {
    board = $('#board');
    sol_board = $('#solution')

    //across listener
    $('#across').on('click', 'li', function () {
        cleanOldChoice();

        var click_src = $(this);
        click_src.addClass('blue');
        var square = board.find('.number[value=' + click_src.data('key') + ']').closest('.square');
        square.addClass('yellow');
        board.find('.square[y=' + square.attr('y') + ']').not('.square.black').addClass('blue');

        square = sol_board.find('.number[value=' + click_src.data('key') + ']').closest('.square');
        square.addClass('yellow');
        sol_board.find('.square[y=' + square.attr('y') + ']').not('.square.black').addClass('blue');
    });

    //down listener
    $('#down').on('click', 'li', function () {
        cleanOldChoice();

        var click_src = $(this);
        click_src.addClass('blue');
        var square = board.find('.number[value=' + click_src.data('key') + ']').closest('.square');
        square.addClass('yellow');
        board.find('.square[x=' + square.attr('x') + ']').not('.square.black').addClass('blue');

        square = sol_board.find('.number[value=' + click_src.data('key') + ']').closest('.square');
        square.addClass('yellow');
        sol_board.find('.square[x=' + square.attr('x') + ']').not('.square.black').addClass('blue');
    });

    board.on('focus', '.square', function () {
        if ($(this).hasClass('black')) {
            return;
        }

        $(this).addClass('selected');
    });

    board.on('focusout', '.square', function() {
        if ($(this).hasClass('black')) {
            return;
        }

        $(this).removeClass('selected');
    });

    board.on('keyup', '.square', function (event) {
        if ($(this).hasClass('black') || !String.fromCharCode(event.which).match(/[a-zA-Z]/i)) {
            $(this).find('.table-cell').text('');
            return;
        }

        $(this).find('.table-cell').text(String.fromCharCode(event.which).toUpperCase());
        $(this).removeClass('wrong').removeClass('correct');
    });
});

//helpers
function cleanOldChoice() {
    board.find('.square.yellow').removeClass('yellow');
    board.find('.square.blue').removeClass('blue');
    sol_board.find('.square.yellow').removeClass('yellow');
    sol_board.find('.square.blue').removeClass('blue');
    $('li.blue').removeClass('blue');
}

//puzzle constructor
function initPuzzle(puzzle) {
    /*puzzle cells*/
    var cells = [];

    //2d to 1d with trusted x,y coordinates
    $.each(puzzle.solution_cells, function(index, item) {
        var trusted_index = (item.y - 1) * 5 + item.x - 1;
        cells[trusted_index] = {key: item.key, solution: item.solution, color: item.color};
    });

    //place them into board
    cleanOldChoice();
    board.prev().html(board.prev().text().split('-')[0] + '- <b class="pull-right">' + puzzle.date + '<b>');
    board.find('.number').removeAttr('value');
    board.find('.square').attr('class', 'square');
    board.find('.table-cell').text('');
    $.each(board.find('.square'), function(index, element) {
        if (cells[index].color === 'black') {
            $(element).addClass('black');
            return;
        }

        var key_holder = $(element).find('.number');
        key_holder.text(cells[index].key);
        key_holder.attr('value', cells[index].key);
        $(element).find('.table-cell').attr('answer', cells[index].solution);
    });

    //also to the solution board
    sol_board.find('.number').removeAttr('value');
    sol_board.find('.square.black').removeClass('black');
    $.each(sol_board.find('.square'), function(index, element) {
        if (cells[index].color === 'black') {
            $(element).addClass('black');
            return;
        }

        var key_holder = $(element).find('.number');
        key_holder.text(cells[index].key);
        key_holder.attr('value', cells[index].key);
        $(element).find('.table-cell').text(cells[index].solution);
    });
    /*--end puzzle cells*/

    /*clues*/
    //empty clue lists
    $('#across .list-group, #down .list-group').empty();

    //across clues
    var clues = "";
    $.each(puzzle.clues.Across, function(index, item) {
        clues += '<li class="list-group-item" data-key="' + item.key + '">' + item.key + ') ' + item.hint + '</li>';
    });
    $('#across').find('.list-group').html(clues);

    //down clues
    clues = "";
    $.each(puzzle.clues.Down, function(index, item) {
        clues += '<li class="list-group-item" data-key="' + item.key + '">' + item.key + ') ' + item.hint + '</li>';
    });
    $('#down').find('.list-group').html(clues);
    /*--end clues*/
}

function checkPuzzle() {
    $.each(board.find('.square').not('.black'), function(index, element) {
        var cell = $(element).find('.table-cell');
        if (cell.text() === '') {
            return;
        }

        if (cell.attr('answer') === cell.text()) {
            $(element).removeClass('wrong').addClass('correct');
        } else {
            $(element).removeClass('correct').addClass('wrong');
        }
    });
}