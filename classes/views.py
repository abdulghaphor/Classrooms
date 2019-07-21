from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Classroom, Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			x = form.save(commit=False)
			x.set_password(x.password)
			x.save()
			login(request, x)
			return redirect('classroom-list')
	context = {
		"form": SignupForm(),
	}
	return render(request, 'signup.html', context)

def signin(request):
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			x = form.cleaned_data['username']
			y = form.cleaned_data['password']
			z = authenticate(username=x, password=y)
			if z is not None:
				login(request, z)
				return redirect('classroom-list')
	context = {
		"form":SigninForm()
	}
	return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect('classroom-list')

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	context = {
		"classroom": classroom,
		'students' : Student.objects.filter(classroom=classroom_id).order_by('exam_grade')
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if not request.user.is_authenticated:
		return redirect('signin')

	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			x = form.save(commit=False)
			x.teacher = request.user
			x.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


def student_add(request,classroom_id):
	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			x = form.save(commit=False)
			x.classroom = Classroom.objects.get(id=classroom_id)
			x.save()
			messages.success(request, "Successfully Added Student!")
			return redirect('classroom-detail',classroom_id)
		print (form.errors)
	context = {
		"form": StudentForm(),
		"classroom" : Classroom.objects.get(id=classroom_id),
	}
	return render(request,'student_add.html', context)

def student_delete(request,classroom_id, student_id):
	Student.objects.get(id=student_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-detail',classroom_id)

def student_update(request, classroom_id, student_id):
	classroom = Classroom.objects.get(id=classroom_id)
	student = Student.objects.get(id=student_id)
	form = StudentForm(instance=student)
	if request.method == "POST":
		form = StudentForm(request.POST,instance=student)
		if form.is_valid():
			c = form.save(commit=False)
			c.classroom = classroom
			c.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-detail',classroom_id)
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	"student" : student,
	}
	return render(request, 'student_update.html', context)