  var app = angular.module('AddStreamApp', []);
  app.controller('AddStreamCtrl', function($scope,$http,$window,$timeout) {
    $scope.showLoader = true;
    $scope.reload = function () {
      $http.get('/supervisord/api/supervisord/').then(function (response) {
        $scope.job_list = response.data.process;
        $scope.showLoader = false;
      });
      $timeout(function(){
        $scope.reload();
      },10000)
    };
    $scope.reload();
    $scope.stream={'source': '', 'stream_type': 'Facebook', 'name': '', 'stream_key': ''};
  //Check keypress is Enter
    $scope.checkIfEnterKeyWasPressed = function($event){
      console.log("Enter");
    };

    $scope.check_empty = function (str){
      if (str == ''){
        return true;
      }
      return false;
    };

    $scope.check_unicode = function (str){
      for (var i = 0; i < str.length; i++) {
        if(str.charCodeAt(i) > 127) {
          return true;
        }
      }
      return false;
    };

    $scope.validate = function () {
      errors = '';
      if ($scope.check_empty($scope.stream.name)){
        errors += "\n" + 'Sorry! Name is empty.';
      }
      if ($scope.check_empty($scope.stream.stream_type)){
        errors += "\n" + 'Sorry! Please select stream type.'
      }
      if ($scope.check_empty($scope.stream.source)){
        errors += "\n" + 'Sorry! Source is empty.'
      }
      if ($scope.check_empty($scope.stream.stream_key)){
        errors += "\n" + 'Sorry! Stream key is empty.'
      }
      if ($scope.check_unicode($scope.stream.name)){
        errors += "\n" + 'Sorry! Name does not support special characters.';
      }
      if ($scope.check_unicode($scope.stream.source)){
        errors += "\n" + 'Sorry! Source does not support special characters.'
      }
      if ($scope.check_unicode($scope.stream.stream_key)){
        errors += "\n" + 'Sorry! Stream key does not support special characters.'
      }
      return errors;
    };
    //save
    $scope.save = function () {
      console.log($scope.stream);
      errors = $scope.validate();
      if (errors == '') {
        console.log($scope.stream);
        $scope.showLoader = true;
        $http({
          method : 'POST',
          url : '/supervisord/',
          data : $scope.stream
        }).then(function(response){
          if(response.status == 203){
            $scope.showLoader = false;
            $window.alert(response.data.detail);
          }
          else
            if (response.status == 202){
              $scope.showLoader = false;
              $window.alert(response.data.detail);
              $('#addModal').modal('hide');
              $scope.stream={'source': '', 'stream_type': 'Facebook', 'name': '', 'stream_key': ''};
              $scope.reload();
            }
        });
      }//end if
      else
      {
        $window.alert(errors);
      }
    };
    //end save 
    //edit
    $scope.edit = function (field) {
      $scope.stream = field;
      $('#addModal').modal('show');
    };
    //end edit
    //delete
    $scope.delete = function (field) {
      if ($window.confirm("Please confirm! remove stream "+field.name+"?")) {
        $http({
          method : 'DELETE',
          url : '/supervisord/api/'+field.name+'/',
        }).then(function(response){
          if(response.status == 203){
            $window.alert(response.data.detail);
          }
          else
            if (response.status == 202){
              $window.alert(response.data.detail);
              $scope.reload();
            }
        });
      }//end if
    };
    //end detele 
    //start
    $scope.start = function (field) {
      if ($window.confirm("Please confirm! start stream "+field.name+"?")) {
        action_content = {'action': 'start'};
        $http({
          method : 'OPTIONS',
          url : '/supervisord/api/'+field.name+'/',
          data : action_content
        }).then(function(response){
          if(response.status == 203){
            $window.alert(response.data.detail);
          }
          else
            if (response.status == 202){
              $window.alert(response.data.detail);
              $scope.reload();
            }
        });
      }//end if
    };
    //end start
    //restart
    $scope.restart = function (field) {
      if ($window.confirm("Please confirm! restart stream "+field.name+"?")) {
        action_content = {'action': 'restart'};
        $scope.showLoader = true;
        $http({
          method : 'OPTIONS',
          url : '/supervisord/api/'+field.name+'/',
          data : action_content
        }).then(function(response){
          if(response.status == 203){
            $scope.showLoader = false;
            $window.alert(response.data.detail);
          }
          else
            if (response.status == 202){
              $scope.showLoader = false;
              $window.alert(response.data.detail);
              $scope.reload();
            }
        });
      }//end if
    };
    //end restart
    //restart
    $scope.stop = function (field) {
      if ($window.confirm("Please confirm! stop strem "+field.name+"?")) {
        action_content = {'action': 'stop'};
        $http({
          method : 'OPTIONS',
          url : '/supervisord/api/'+field.name+'/',
          data : action_content
        }).then(function(response){
          if(response.status == 203){
            $window.alert(response.data.detail);
          }
          else
            if (response.status == 202){
              $window.alert(response.data.detail);
              $scope.reload();
            }
        });
      }//end if
    };
    //end restart
  });