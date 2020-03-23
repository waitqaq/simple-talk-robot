$(function () {
    $('.SAVE').on('click',(e)=>{
        e.preventDefault();
        $.ajax({
            url: '/config',
            type: 'POST',
            data: {'config':$('#config-input').val()},
            success: function (res) {
                var data = JSON.parse(res);
                if (data.code == 0){
                    console.log('配置写入成功')
                    alert('配置写入成功,请重启生效')
                }else{
                    console.error('配置写入失败')
                    alert('配置写入失败')
                }
            },
            error: function () {
                console.error('配置写入失败')
            }
        })
    });
        $('.RESTART').on('click',(e)=>{
        e.preventDefault();
        $.ajax({
            url: '/operate',
            type: 'POST',
            success: function (res) {
                var data = JSON.parse(res);
                if (data.code == 0){
                    console.log('重启成功')
                    alert('重启成功')
                }else{
                    console.error('重启失败')
                }
            },
            error: function () {
                console.error('重启失败')
            }
        })
    });
});