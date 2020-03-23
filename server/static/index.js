function appendHistory(type,query, uuid) {
    if (query=='' || !uuid) return;
    if (type==0){
        //用户消息
        $('.history').append(`
          <div class="right">
            <div class="bubble-green">
              <div class="bubble-avatar"><i class="fas fa-user"></i></div>
              <p style="text-align: left" id="${uuid}">${query}</p>
            </div>
          </div>
        `)
    }else {
        // 机器人消息
        $('.history').append(`
         <div class="left">
            <div class="bubble-white">
              <div class="bubble-avatar"><i class="fas fa-robot"></i></div>
              <p style="text-align: left" id="${uuid}">${query}</p>
            </div>
         </div>
        `)
    }
    var scrollHeight = $('.history').prop('scrollHeight')
    $('.history').scrollTop(scrollHeight, 500);
}

function getHistory(){
    $.ajax({
        url:'/history',
        type:'GET',
        success: function (res) {
            res = JSON.parse(res);
            if (res.code == 0){
                historyList = JSON.parse(res.history);
                for (let i=0; i<historyList.length; ++i){
                    h = historyList[i];
                    // 是否已经存于页面
                    if (!$('.history').find('#'+h['uuid']).length>0){
                        //添加气泡
                        appendHistory(h['type'],h['text'], h['uuid']);
                    }
                }
            }else{
                console.error('获取历史信息失败')
            }
        },
        error:function () {
            console.error('获取历史信息失败')
        }
    })
}

$(function(){
    setInterval('getHistory();', 5000);
    $('.CHAT').on('click', function (e) {
        e.preventDefault();
        var query = $('input#query')[0].value;
        $('input#query').val('');
        args = {'query':query};
        $.ajax({
            url: '/chat',
            type: 'POST',
            data: $.param(args),
            success: function (res) {
                var data = JSON.parse(res);
                if (data.code == 0){
                    console.log('指令发送成功')
                }else{
                    console.error('指令发送失败')
                }
            },
            error: function () {
                console.error('指令发送失败')
            }
        })
    })
});