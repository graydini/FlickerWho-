myGame = new Object();
base_url = "/";
function recieve_chat(message){}
function recieve_guess(guess){}
function recieve_scores(scores){}
function start_game(opponent){
if (opponent != undefined){ params = {'opponent':opponent};}
else params = {};
$.get(base_url+'game/board',params,function(data){
	if(data != "failed"){
		myGame = data;
	}
	else{
	alert("Somthing has gone wrong, sorry!");
	}
	},"json");
}
function recieve_answer(answer){}
function recieve_clue(clue){}
function send(command,message){
$.get(base_url+'game'+command,{'game_id':myGame.id})
}
function poll(){
$.get(base_url+'game/poll', function(data){
	if (data != ""){
		for(message in data){
			if(data[message]['chat'] != undefined){ recieve_chat(data[message]);}
			else if (data[message]['answer'] != undefined){ recieve_answer(data[message]['answer']);}
			else if (data[message]['guess'] != undefined){ recieve_guess(data[message]['guess']);}
			else{
			recieve_clue(data[message]['clue']);
			}
			
			
		}
	}

},"json");

}
