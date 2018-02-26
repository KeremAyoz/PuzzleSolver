var board;
//listeners
$(function() {
    board = $('#board');

    //across listener
    $('#across').on('click', 'li', function () {
        cleanOldChoice();

        var click_src = $(this);
        click_src.addClass('blue');
        var square = board.find('.number[value=' + click_src.data('key') + ']').closest('.square');
        square.addClass('yellow');
        board.find('.square[y=' + square.attr('y') + ']').not('.square.black').addClass('blue');
    });

    //down listener
    $('#down').on('click', 'li', function () {
        cleanOldChoice();

        var click_src = $(this);
        click_src.addClass('blue');
        var square = board.find('.number[value=' + click_src.data('key') + ']').closest('.square');
        square.addClass('yellow');
        board.find('.square[x=' + square.attr('x') + ']').not('.square.black').addClass('blue');
    });
});

//helpers
function cleanOldChoice() {
    board.find('.square.yellow').removeClass('yellow');
    board.find('.square.blue').removeClass('blue');
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
    board.find('.square.black').removeClass('black');
    $.each(board.find('.square'), function(index, element) {
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