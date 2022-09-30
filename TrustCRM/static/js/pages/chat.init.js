const ChatIcon=($id,$array,$el,$cond)=>{
    var listItems = document.getElementById($id).children;
    //var  w = document.getElementById($id).children;
    
    var colors = $array;
    var j=0;
    for( i= 0; i < listItems.length; i ++)  {

        //For Chat Block left
        $(listItems[i].querySelectorAll($el)).css("backgroundColor",colors[j]);

        //For Chat Block right
        if($cond){
            
            
            if($(listItems[i]).hasClass('right')){
                $(listItems[i].querySelectorAll($el)).addClass('text-white');
                $(listItems[i].querySelectorAll($el)).css("backgroundColor",$array[0]);
                $(listItems[i].querySelectorAll($el)).css("marginRight",'0px');
                $(listItems[i].querySelectorAll($el)).css("max-width",'80%');
                $(listItems[i].querySelectorAll($el)).css("borderRadius",'4px');
                let innerWidth=$(listItems[i].querySelector($el)).innerWidth();
                $(listItems[i].querySelector('.conversation-name')).css('width',innerWidth );
               
                
                
            // $(listItems[i].querySelectorAll($el).querySelector('.user-name')).addClass('text-white');
                //$(listItems[i].querySelectorAll($el)).("::after",'0px');
            }else if($(listItems[i]).hasClass('left')){

                $(listItems[i].querySelectorAll($el)).addClass('color-color1');
                $(listItems[i].querySelectorAll($el)).css("backgroundColor",$array[1]);
                $(listItems[i].querySelectorAll($el)).css("max-width",'80%');
                $(listItems[i].querySelectorAll($el)).css("marginLeft",'0px');
                $(listItems[i].querySelectorAll($el)).css("borderRadius",'4px');
                let innerWidth=$(listItems[i].querySelector($el)).innerWidth();
                $(listItems[i].querySelectorAll('.conversation-name')).css('width',innerWidth );
                
               
            }
        }
        
        
        j++;  
        if (j==colors.length) {
            j=0;  
        }     
        
    }

}
//chat 

$(document).ready(function () {

    //chat 
    //need to call on everytime this tab click
    ChatIcon('chat-list',["#9296F3", "#9FE0AB", "#78CCF6", "#EE817F"],'.avatar-title');

    //chatarchive 
    //need to call on everytime this tab click
    ChatIcon('archive-list',["#9296F3", "#9FE0AB", "#78CCF6", "#EE817F"],'.avatar-title');

    //chatcont
    //need to call on each chat click
    ChatIcon('chat-conversation',["#43456C","#232436"],'.ctext-wrap-content','chat-conversation');

    //chat 
    //need to call on everytime this tab click
    const simpleBarMessagelist = new SimpleBar(document.getElementById('chat-message-list'));

    //chatarchive 
    //need to call on everytime this tab click
    const simpleBarMessagelistarchive = new SimpleBar(document.getElementById('chat-message-list-archive'));
    
   
    //chatcont
    //need to call on each chat click
    const simpleBarChatconversationWrap = new SimpleBar(document.getElementById('chat-conversation-wrap'));
    simpleBarChatconversationWrap.getScrollElement().scrollTop =  simpleBarChatconversationWrap.getScrollElement().scrollHeight;
  
});