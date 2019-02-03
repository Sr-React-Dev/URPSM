$(function () {
  var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      var matches, substringRegex;
      matches = [];
      substrRegex = new RegExp(q, 'i');
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          matches.push({ value: str });
        }
      });
      cb(matches);
      // console.log(matches);
    };
  };


   $.ajax({
    url: AUTOCOMPLETE_URL,
    cache: false,
    error:function(xhr, error, _){
      console.log(xhr, error);
    },
    success: function (data) {
      console.log(data);
      $('#query').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
      },
      {
        name: 'data',
        displayKey: 'value',
        source: substringMatcher(data)
      });
    }
  });

  $(document).on('keypress', function(e) {
    if(e.which == 13) {
        if($('#query').is(":focus")){
          console.log($('#query').val());
          
        }
      }
      // e.preventDefault();
    });
  $(document).on('click', function(e) {
    if(e.which == 13) {
        if($('#from').is(":focus")){
          console.log($('#from').val());
        }
      }
      // e.preventDefault();
    });




});

//    $('#from').on('change',function(){
//    });
// if($('#from').is(":focus")){
//    $('#from').on('change',function(){
//     console.log($(this).val());
//    });