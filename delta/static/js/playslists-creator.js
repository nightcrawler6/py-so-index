$(document).ready(function() {
    $('.play a').on("click", function(event){
        var obj = $(event.target).parent().parent().parent()[0];

        var objId = obj.id;
        var allCards = $('.play');
        var toHide = [];
        for (var i = 0; i < allCards.length; i++){
            var cur = allCards[i];
            if (cur.id == objId){
                continue;
            }
            else{
                if($(cur).css('display')=='none'){
                    $(cur).css('display','block');
                }
                else {
                    $(cur).css('display', 'none');
                }
            }
        }
        if($("#amazing-table").css('display')=='none'){
            $($("#amazing-table")[0]).fadeIn();
        }
        else {
            $($("#amazing-table")[0]).css('display','none');
        }
    })
});