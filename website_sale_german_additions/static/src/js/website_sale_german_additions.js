jQuery("document").ready(function($) {

	if($("#revbox").length != 0) {
		//check if revocation checkbox is checked and stop submit
		$("form").submit(function(e) {
			if(!$('#revbox').attr('checked')) {
				e.preventDefault();
				$('#revlabel').addClass('has-error');
				$('#rev').addClass('has-error');
			}
		});
	};
    
    //show and hide functions for the terms and revocation popup
    $("#close-terms").click(function() {
        $("#wsga-terms").hide("slow");
    });    
        
    $("#open-terms").click(function() {
        $("#wsga-terms").show("slow");
    });
    
    $("#close-revo").click(function() {
        $("#wsga-revo").hide("slow");
    });    
        
    $("#open-revo").click(function() {
        $("#wsga-revo").show("slow");
    });
	
});