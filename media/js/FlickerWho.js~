myGame = new Object();
players = [];
base_url = "/";
function update_player_list(){}
function recieve_chat(message){}
function recieve_guess(guess){}
function recieve_scores(scores){}
function start_game(opponent){
if (opponent != undefined){ params = {opponent:opponent};}
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
if (command=="choose"){
$.get(base_url+'game/board',{game_id:myGame.id, choice:message});
}
$.get(base_url+'game'+command+'?'+message,{game_id:myGame.id,opponent=myGame.opponent},function(data){
	switch(command){
		case "players":
			players = data;
			update_player_list();
			break;
		case "guess":
				if (data != ""){
				
				}
			break;
		case "respond":
			break;
	}
	},"json");
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
