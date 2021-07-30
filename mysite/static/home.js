if (typeof App == "undefined") var App = {};
var App = {
    myPar: function(e) {

        var formData = new FormData()
        var par = document.querySelector('#choice_par')
        formData.append('action', 'save_par')
        formData.append('choice_par', event.target.value)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },
    
    myDur: function(e) {

        var formData = new FormData()
        var dur = document.querySelector('#choice_dur')
        formData.append('action', 'save_dur')
        formData.append('choice_dur', event.target.value)
        formData.append('check_dur', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    myCrec: function(e) {

        var formData = new FormData()
        var appr = document.querySelector('#choice_appr')
        formData.append('action', 'save_appr')
        formData.append('choice_appr', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    myAtt: function(e) {

        var formData = new FormData()
        var att = document.querySelector('#choice_att')
        formData.append('action', 'save_att')
        formData.append('choice_att', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    myBor: function(e) {

        var formData = new FormData()
        var bor = document.querySelector('#choice_bor')
        formData.append('action', 'save_bor')
        formData.append('choice_bor', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    mySta: function(e) {

        var formData = new FormData()
        var stage = document.querySelector('#choice_stage')
        formData.append('action', 'save_stage')
        formData.append('choice_stage', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    myCert: function(e) {

        var formData = new FormData()
        var cert = document.querySelector('#choice_cert')
        formData.append('action', 'save_cert')
        formData.append('choice_cert', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    myTut: function(e) {

        var formData = new FormData()
        var tut = document.querySelector('#choice_tut')
        formData.append('action', 'save_tut')
        formData.append('choice_tut', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },


    myDist: function(e) {

        var formData = new FormData()
        var dist = document.querySelector('#choice_dist')
        formData.append('action', 'save_dist')
        formData.append('choice_dist', event.target.value)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },
    cannotEnter(){
        $('.cannotEnter').addClass('active')
        $('.blackout').addClass('active')
    },
    canEnter(position){
        var vm = this;
        var lat = 0;
        var lon = 0;
        $('.cannotEnter').removeClass('active')
        $('.blackout').removeClass('active')
        if(position){
            lat = position.coords.latitude;
            lon = position.coords.longitude;
            vm.inviaDati([lat,lon])
        }
    },
    getLocation() {

        var vm = this;
        if('permissions' in navigator){
            navigator.permissions.query({name:'geolocation'}).then(function(result) {
                // Will return ['granted', 'prompt', 'denied']
                if (result.state == "denied"){
                    vm.cannotEnter()
                }
               
             
                navigator.geolocation.getCurrentPosition(function(position){

                    if (result.state=='granted') {
                        vm.canEnter(position)
                    }
       
                })
                result.onchange = function(r) {
                   if (r.target.state == "denied"){
                       vm.cannotEnter()
                   }
                   console.log(r.target.state)
                   if (r.target.state == "granted") {
                        vm.canEnter()
                   }
                }
            })
            
        } else {
            // ask for location
           var user_posi =  navigator.geolocation
           if (user_posi) {
                navigator.geolocation.getCurrentPosition(function(position){
                    vm.canEnter(position)
                })
           } else {
               document.body.innerHTML = "Non hai i requisiti necessari per accedere al sito, utilizza Chrome/Firefox";
           }
   
            
        }
    },
    inviaDati(params){
        var formData = new FormData()
        formData.append('action', 'save_position')
        formData.append('lat', params[0])
        formData.append('lon', params[1])
        formData.append('user_id', user_id)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
        
    },
    myPos: function(e) {
    },

    myReset: function(e) {
        var formData = new FormData()
        var reset = document.querySelector('#choice_reset')
        formData.append('action', 'save_reset')
        formData.append('choice_reset', event.target.value)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    // Materie
    mySub: function(e) {

        var formData = new FormData()
        var sub = document.querySelector('#choice_sub')
        formData.append('action', 'save_sub')
        formData.append('choice_sub', event.target.value)
        formData.append('check_sub', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    myParSub: function(e) {

        var formData = new FormData()
        var parsub = document.querySelector('#choice_parsub')
        formData.append('action', 'save_parsub')
        formData.append('choice_parsub', event.target.value)
        formData.append('check_parsub', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    // Dettagli interesse
    myAI: function(e) {

        var formData = new FormData()
        var ai = document.querySelector('#choice_ai')
        formData.append('action', 'save_ai')
        formData.append('choice_ai', event.target.value)
        formData.append('check_ai', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    myDetAI: function(e) {

        var formData = new FormData()
        var detai = document.querySelector('#choice_detai')
        formData.append('action', 'save_detai')
        formData.append('choice_detai', event.target.value)
        formData.append('check_detai', event.target.checked)
        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    },

    myUpdate: function(e) {

        function objLength(obj){
            var i=0;
            for (var x in obj){
              if(obj.hasOwnProperty(x)){
                i++;
              }
            } 
            return i;
        }

        setTimeout(filterData, 1000)
        function filterData() {
            axios.post('/filtered_data/', null, {headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
                // handle success
                var json_file = response.data
                var genAIcheckboxes = "";
                for (var i=0;i<json_file.AI.db.length; i++) {
                    var val_ai = json_file.AI.db[i];
                    var is_check = json_file.AI.selected.filter((item) => item.name_ai == val_ai).length > 0;
                    var is_check = (is_check) ? 'checked' : '';
                    genAIcheckboxes = genAIcheckboxes + `<div><input ${is_check} class="form-check-input" name="choice_ai" type="checkbox" id="choice_ai" value="${val_ai}"> 
                    <label class="form-check-label" for="flexCheckDefault">${val_ai}</label> </div>`;
                };
                $('#areainteresse').html(genAIcheckboxes)

                var genDetAIcheckboxes = "";
                for (var i=0;i<json_file.DetAI.db.length; i++) {
                    var val_detai = json_file.DetAI.db[i];
                    var is_check = json_file.DetAI.selected.filter((item) => item.det_ai == val_detai).length > 0;
                    var is_check = (is_check) ? 'checked' : '';
                    genDetAIcheckboxes = genDetAIcheckboxes + `<div><input ${is_check} class="form-check-input" name="choice_detai" type="checkbox" id="choice_detai" value="${val_detai}"> 
                    <label class="form-check-label" for="flexCheckDefault">${val_detai}</label> </div>`;
                };
                $('#dettagliareainteresse').html(genDetAIcheckboxes)

                var genParSubcheckboxes = "";
                for (var i=0;i<json_file.ParSub.db.length; i++) {
                    var val_parsub = json_file.ParSub.db[i];
                    var is_check = json_file.ParSub.selected.filter((item) => item.parsub == val_parsub).length > 0;
                    var is_check = (is_check) ? 'checked' : '';
                    genParSubcheckboxes = genParSubcheckboxes + `<div><input ${is_check} class="form-check-input" name="choice_parsub" type="checkbox" id="choice_parsub" value="${val_parsub}"> 
                    <label class="form-check-label" for="flexCheckDefault">${val_parsub}</label> </div>`;
                };
            $('#parent_subject').html(genParSubcheckboxes)

                var genSubcheckboxes = "";
                for (var i=0;i<json_file.Sub.db.length; i++) {
                    var val_sub = json_file.Sub.db[i];
                    var is_check = json_file.Sub.selected.filter((item) => item.name_sub == val_sub).length > 0;
                    var is_check = (is_check) ? 'checked' : '';
                    genSubcheckboxes = genSubcheckboxes + `<div><input ${is_check} class="form-check-input" name="choice_sub" type="checkbox" id="choice_sub" value="${val_sub}"> 
                    <label class="form-check-label" for="flexCheckDefault">${val_sub}</label> </div>`;
                };
                $('#subject').html(genSubcheckboxes)

                genLen = json_file.lunghDF
                $('#lunghezzaOn').html(genLen)
                
                var genDF = "";
                if (json_file.lunghDF != 0) {
                    for (var i=0;i<objLength(json_file.mainDF.d); i++) {
                        genDF = genDF + '<ul class="list-group">'+
                        '<li class="list-group-item">'+ json_file.mainDF.d[i].school_name +'</li>'+
                        '</ul>'
                    }
                } else {
                    genDF = '<p> La ricerca non ha prodotto risultati </p>'+'<ul class="list-group">'+
                    '<li class="list-group-item"> </li> </ul>'
                }
                $('#risultati').html(genDF)
            })
            .catch(function(error) {
                // handle error
                console.log(error);
            })
            .then(function() {
                // always executed
            });
        }
    },


    setup: function() {
        this.getLocation();
        var vm = this;

        vm.myUpdate()

        $('#dist').on('click', function(e){
            vm.myPos(e)
        }),

        $('input[name="choice_par"]').on('change', function(e){
            vm.myPar(e)
        }),
        
        $('input[name="choice_dur"]').on('change', function(e){
            vm.myDur(e)
        }),

        $('input[name="choice_appr"]').on('change', function(e){
            vm.myCrec(e)
        }),

        $('input[name="choice_att"]').on('change', function(e){
            vm.myAtt(e)
        }),

        $('input[name="choice_bor"]').on('change', function(e){
            vm.myBor(e)
        }),

        $('input[name="choice_stage"]').on('change', function(e){
            vm.mySta(e)
        }),

        $('input[name="choice_cert"]').on('change', function(e){
            vm.myCert(e)
        }),

        $('input[name="choice_tut"]').on('change', function(e){
            vm.myTut(e)
        }),

        $('input[name="choice_dist"]').on('change', function(e){
            vm.myDist(e)
        }),

        $('input[name="choice_dist"]').on('change', function(e){
            vm.myPos(e)
        }),

        $('input[name="choice_reset"]').on('change', function(e){
            vm.myReset(e)
        }),

        $(document).on("change",'input[name="choice_sub"]', function(e){
            vm.mySub(e)
        }),

        $(document).on("change",'input[name="choice_parsub"]', function(e){
            vm.myParSub(e)
        }),

        $(document).on("change",'input[name="choice_ai"]', function(e){
            vm.myAI(e)
        }),

        $(document).on("change",'input[name="choice_detai"]', function(e){
            vm.myDetAI(e)
        })
        
    },

}


window.onload = function() {
    
    var lat = 0;
    var lon = 0;
    var csrftoken = '{{csrf_token}}';

    var formData = new FormData()

    function inviaDati(params){
        formData.append('action', 'save_position')
        formData.append('lat', params[0])
        formData.append('lon', params[1])
        formData.append('user_id', '{{request.user.id}}')


        axios.post('/salvadati/', formData,{headers: {'X-CSRFToken': csrftoken}}).then(function(response) {
            // handle success
            console.log(response.data.response);
        })
        .catch(function(error) {
            // handle error
            console.log(error);
        })
        .then(function() {
            // always executed
        });
    }
    function geta(position) {
        lat = position.coords.latitude;
        lon = position.coords.longitude;
        var res = [lat,lon]
        inviaDati([lat,lon])
        return lat, lon;
    }

}