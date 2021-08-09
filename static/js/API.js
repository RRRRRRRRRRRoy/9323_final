let basic = "http://127.0.0.1:5000/";
let API = {
    saveSession: function (key,data){
        // Save the data and key in the window
        // Source: https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage
        let Jsonified_data = JSON.stringify(data);
        sessionStorage.setItem(key, Jsonified_data);
    },
    getSession: function (key){
        // Using the sessionStorage to store
        // return the JSONified data data
        let session_stored_key = sessionStorage.getItem(key);
        return JSON.parse(session_stored_key);
    },
    saveUserInfo: function (data) {
        // Save the data in the window session
        // Source: // Source: https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage
        let user_information_data = data;
        sessionStorage.setItem("user", user_information_data);
    },
    getUserInfo: function () {
        // Using JSON.parse() to change the JSON type data
        // Source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse
        let session_stored_key = sessionStorage.getItem("user");
        let jsonified_key_data = JSON.parse(session_stored_key);
        return jsonified_key_data;
    },
    savegroupin: function (data) {
        // Similarly with the previous usage
        let group_information_data = data;
        sessionStorage.setItem("groupin", group_information_data);
    },
    getgroupinfo: function () {
        // getting the group data
        let session_stroed_groupinfo = sessionStorage.getItem("groupin");
        let jsonified_group_data = JSON.parse(session_stroed_groupinfo);
        return jsonified_group_data;
    },
    clearUserInfo: function (){
        // Remove all saved data from sessionStorage
        // Source: https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage
        sessionStorage.clear();
    },
    personal: function () {
        // retriving the user information
        let user = this.getUserInfo();
        // check the current user is null or not
        // if null remove 
        if (user == null) {
            $("#personal").remove();
            $("#signOut").remove();
        }
        // else show the username
        if (user != null) {
            // the current user is login
            let user_name = user.userinfo.name;
            // hide the login and signup
            $("#loginSignUp").remove();
            // show the personal user name instead
            $("#personal").text(user_name);
        } 
    },
    toJson: function (data) {
        // Setting a dictionary to store the data
        let JsonifiedStr = {};
        $.each(data, function() {
            // the current key of the dict
            current_key = this.name;
            // the current value of the dict
            current_value = this.value;
            JsonifiedStr[current_key] = current_value;
        });
        return JsonifiedStr;
    },
    // the structure of Ajax used in JQuery
    // Source: https://stackoverflow.com/questions/23682438/proper-ajax-get-structure-using-jquery
    // Source: https://www.tutorialrepublic.com/jquery-tutorial/jquery-ajax-get-and-post-requests.php
    get: function (url,data,successCallback) {
        // getting the data from the server
        let user_info_request = this.getUserInfo();
        if(user_info_request != null){
            // Using ajax get data
            $.ajax({
                type : "GET",
                headers: {
                    // not null need a token to check
                    "token":user_info_request.token
                },
                contentType: "application/json;charset=UTF-8",
                url : basic + url,
                dataType: 'JSON',
                data : data,
                success : function(result) {
                    // if success
                    successCallback(result);
                },
                error : function(e){
                    // if fail
                    let status = e.status;
                    let responseText = e.responseText;
                    console.log(status);
                    console.log(responseText);
                }
            });
        }
        // the current user is null
        // Source: https://www.w3schools.com/jquery/jquery_ajax_get_post.asp
        if (user_info_request == null) {
            // using ajax to get data without token
            $.ajax({
                type : "GET",
                contentType: "application/json;charset=UTF-8",
                url : basic + url,
                dataType: 'JSON',
                data : data,
                success : function(result) {
                    // if success
                    successCallback(result);
                },
                error : function(e){
                    // if fail
                    let status = e.status;
                    let responseText = e.responseText;
                    console.log(status);
                    console.log(responseText);
                }
            });
        }
    },
    // JQuert.Ajax() post data to server
    // https://www.freecodecamp.org/news/jquery-ajax-post-method/
    post: function (url,data,successCallback) {
        // post the data to server
        $.ajax({
            type : "POST",
            contentType: "application/json;charset=UTF-8",
            url : basic + url,
            dataType: 'JSONP',
            data : JSON.stringify(data),
            success : function(result) {
                // if success
                successCallback(result);
            },
            error : function(e){
                // if fail
                let status = e.status;
                let responseText = e.responseText;
                console.log(status);
                console.log(responseText);
            }
        });
    },
    postfile: function (url,formData,successCallback) {
        // post the filedata to server
        $.ajax({
            type : "POST",
            url : basic + url,
            async: false,
            dataType:"JSON",
            processData: false,
            contentType: false,
            success : function(result) {
                // if success
                successCallback(result);
            },
            error : function(e){
                // if fail
                let status = e.status;
                let responseText = e.responseText;
                console.log(status);
                console.log(responseText);
            }
        });
    },
}