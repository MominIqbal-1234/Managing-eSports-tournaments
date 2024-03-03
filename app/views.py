
        
from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib import messages
from app.models import CreateTournament,CreateTeam,PlacePointsImage,TempEnterResult,PlacePoints,Result
from django.db.models import Count,Sum
from PIL import Image, ImageDraw, ImageFont

class Home(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request,'homepage_1.html')



class Createtournament(View):
    def get(self,request):
        range = CreateTournament.objects.filter(
            user=request.user
            ).count()
        if range >= 5:
            messages.success(request, 'Limit Exceed Allow 5 ')
            return redirect('/')
        return render(request,'create_tornment.html')
    def post(self,request):
        tornament_name = request.POST['tornament_name']
        organizer_name = request.POST['organizer_name']
        battle_royale_type = request.POST['battle_royale_type']
        teams_info = request.POST['teams_info']
        minimum_players_team = request.POST['minimum_players_team']
        # field_1 = request.POST['field_1']
        if teams_info == 'choose_range':
            messages.error(request, 'Choose Number of Team')
            return redirect('create_tornment')
        elif battle_royale_type == 'SOLO':
            messages.error(request, 'SOLO (Coming Soon)')
            return redirect('create_tornment')
        elif battle_royale_type == 'DUO':
            messages.error(request, 'DUO (Coming Soon)')
            return redirect('create_tornment')
        elif CreateTournament.objects.filter(tournament_name=tornament_name,user=request.user):
            messages.error(request, 'Change Tornament Already Available')
            return redirect('create_tornment')
        CreateTournament(
            tournament_name=tornament_name,
            organizer_name=organizer_name,
            battle_type=battle_royale_type,
            number_of_team=teams_info,
            maximum_player_per_team=minimum_players_team,
            user=request.user
            ).save()
        messages.success(request, 'Tournament Create Successfully')
        return redirect('/')


class Dashboard(View):
    def get(self,request):
        if request.user.is_authenticated:
            tornament = CreateTournament.objects.filter(user=request.user)
            context = {
                'tornament':tornament
            }
            return render(request,'dashboard.html',context)
        return render(request,'homepage_1.html')

class AddTeam(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            team = CreateTeam.objects.filter(createtournament=id)
            context = {
                'team':team,
                'id':id
            }
            return render(request,'add_team.html',context)
    def post(self,request,id):
        if request.user.is_authenticated:
            
            team_name = request.POST['team_name']
            if CreateTeam.objects.filter(team_name=team_name,createtournament_id=id).exists():
               messages.success(request, 'Team Name Already Available')
               return redirect(request.META.get('HTTP_REFERER'))
            

            else:
                count = CreateTournament.objects.get(id=id,user=request.user)
                CreateTeam_Counter = CreateTeam.objects.filter(createtournament_id=id).count()
                if int(count.number_of_team) <= int(CreateTeam_Counter):
                    messages.success(request, 'Team Limit is Full')
                    return redirect(request.path)

                team = CreateTeam(createtournament_id=id,team_name=team_name).save()
                team = CreateTeam.objects.filter(createtournament=id)
                context = {
                    'team':team,
                    'id':id
                }
                messages.success(request, 'Team Add Successfully')
                return render(request,'add_team.html',context)
        

class AddScore(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            countValue = Result.objects.values('match').annotate(count=Count('match')).filter(tourament_id_id=id).last()
            
            result = TempEnterResult.objects.filter(tourament_id_id=id)

            if countValue:
                countValue = countValue['match']
                countValue = int(countValue) + 1
            else:
                countValue = 0
                countValue = countValue + 1
                
            context = {
                'result':result,
                'id':id,
                'countValue':countValue
                
            }
            return render(request,'addscore.html',context)
            
    def post(self,request,id):
        if request.user.is_authenticated:
            team_name = request.POST['team_name']
            id = request.POST['id']
            kill = request.POST['kill']
            match = request.POST['match']
            
            if CreateTeam.objects.filter(team_name=team_name).exists() == False:
               messages.success(request, 'Team not Available')
               return redirect(request.META.get('HTTP_REFERER'))
            elif TempEnterResult.objects.filter(team_name=team_name).exists():
                messages.success(request, 'Team Already Available')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                countValue = TempEnterResult.objects.filter(tourament_id_id=id).count()
                
                points = (PlacePoints.objects.all()[countValue].points)
                
                totalKill = int(kill) + int(points)

                TempEnterResult(
                    team_name=team_name,
                    total=totalKill,
                    kill=kill,
                    place_points=points,
                    tourament_id_id=id,
                    match=match
                    ).save()

                
                countValue = Result.objects.values('match').annotate(count=Count('match')).filter(tourament_id_id=id).last()
                
                result = TempEnterResult.objects.filter(tourament_id_id=id)
                if countValue:
                    countValue = countValue['match']
                    countValue = int(countValue) + 1
                else:
                    countValue = 0
                    countValue = countValue + 1
                    

                context = {
                    'result':result,
                    'id':id,
                    'team_name':team_name,
                    'countValue':countValue
                
                }
                return render(request,'addscore.html',context)
        

class ResultMatch(View):
    def get(self,request,match):
        data = TempEnterResult.objects.filter(match=match)
        for i in data:
            Result(
                team_name=i.team_name,
                place_points=i.place_points,
                kill=i.kill,
                total=i.total,
                match=i.match,
                tourament_id_id=i.tourament_id_id,
                user=request.user
            ).save()
            TempEnterResult.objects.filter(match=match).delete()
        return redirect(request.META.get('HTTP_REFERER'))



class ViewMatch(View):
    def get(self,request,id):
        data = Result.objects.values('tourament_id','match').distinct().filter(tourament_id_id=id,user=request.user)
        match = CreateTeam.objects.filter(createtournament_id=id).count()
        context = {
            'data':data,
            'tourament_id':id,
            'match':match
        }
        return render(request,'view_match.html',context)

class ViewMatchTable(View):
    def get(self,request,id,match):
        result = Result.objects.filter(tourament_id=id,match=match)
        context = {
            'result':result
        }
        return render(request,'view_match_table.html',context)

class ViewPointTable(View):
    def get(self,request,id,match):
        values = []
        
        result = Result.objects.filter(tourament_id=id)
        for i in result:
            place_points = 0
            kill = 0
            total = 0
            team_data = Result.objects.filter(team_name=i.team_name,tourament_id=id)
            for e in team_data:
            
                place_points = place_points + int(e.place_points)
                kill = kill + int(e.kill)
                total = total + int(e.total)
                    
            values.append([i.team_name,place_points,kill,total])
            
        data = (values[:int(match)])
        sorted_data = sorted(data, key=lambda x: x[2],reverse=True)
    
        
        context = {
            'result':sorted_data,
            'id':id,
            'match':match
        }
        return render(request,'view_point_table.html',context)




class ViewPointTableImage(View):
    def get(self,request,id,match):
        values = []
        
        result = Result.objects.filter(tourament_id=id)
        for i in result:
            place_points = 0
            kill = 0
            total = 0
            team_data = Result.objects.filter(team_name=i.team_name,tourament_id=id)
            for e in team_data:
            
                place_points = place_points + int(e.place_points)
                kill = kill + int(e.kill)
                total = total + int(e.total)
                    
            values.append([i.team_name,place_points,kill,total])
            
        data = (values[:int(match)])
        sorted_data = sorted(data, key=lambda x: x[2],reverse=True)
       
        
        
        img = Image.open("static/demo/demo.jpeg")
        font = ImageFont.truetype('static/fonts\\Oswald-Bold.ttf', 30)
        font2 = ImageFont.truetype('static/fonts\\Oswald-Bold.ttf', 20)
        d = ImageDraw.Draw(img)
        
        
        index = 0
        for i in sorted_data:
            grap_value_index = 0
            for e in range(1,5):
                
                values = PlacePointsImage.objects.all()[index]
                d.text((int(values.width),int(values.height)), f"{i[grap_value_index]}",font=font,fill=("black"))
                grap_value_index = grap_value_index + 1
                index = index + 1

        img.save(f'static/scoure_image/{request.user.username}.jpg')
        
        domain = request.META['HTTP_HOST']
        context = {
            'src':f'{domain}/static/scoure_image/{request.user.username}.jpg'
        }
        return render(request,'view_point_table_image.html',context)



class Delete(View):
    def get(self,request,id):
        CreateTournament.objects.get(id=id).delete()
        return redirect(request.META.get('HTTP_REFERER'))

class DeleteTeam(View):
    def get(self,request,id):
        CreateTeam.objects.get(id=id).delete()
        return redirect(request.META.get('HTTP_REFERER'))

class DeleteResult(View):
    def get(self,request,id):
        TempEnterResult.objects.get(id=id).delete()
        return redirect(request.META.get('HTTP_REFERER'))


        