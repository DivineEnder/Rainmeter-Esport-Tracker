$(function(){$("#content").on("click",".spoiler",function(){var a=$(this).closest("tr").children("td.betting");a.find(".currency-bet").fadeOut(200);setTimeout(function(){a.children(".bet-opt").switchClass("","displayed",200);a.find(".currency-result").fadeIn(200)},200)});$("#content").on("click",".spoiler-showall-trigger",function(){var a=$(this).closest("div.box").find("td.betting");if($($(this).find("span.show")[0]).is(":visible")){a.each(function(){$(this).find(".currency-bet").fadeOut(200)});setTimeout(function(){a.each(function(){$(this).children(".bet-opt").switchClass("","displayed",200);$(this).find(".currency-result").fadeIn(200)})},200)}else{a.each(function(){$(this).children(".bet-opt").switchClass("displayed","",200);$(this).find(".currency-result").fadeOut(200)});setTimeout(function(){a.each(function(){$(this).find(".currency-bet").fadeIn(200)})},200)}})});