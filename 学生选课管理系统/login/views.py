from django.shortcuts import render
from django.shortcuts import reverse,redirect
from django.http import HttpResponse, HttpResponseRedirect

from login.forms import StuLoginForm, TeaLoginForm, StuRegisterForm, TeaRegisterForm,createCourse,PasswordChangeForm
from login.models import student,teacher,course,SC
from constants import INVALID_KIND
from django.views.generic import CreateView, UpdateView
from django.db import connection

# Create your views here.

def stuRegister(request):
    return render(request, 'sturegister.html')


def loginPage(request):
    form = StuLoginForm(data=request.POST)
    return render(request,'loginPage.html')

def teacherlogin(request):
    form=TeaLoginForm(data=request.POST)
    if request.method=='POST':
        if form.is_valid():
            tno = form.cleaned_data["tno"]
            if len(tno) != 10:
                form.add_error("tno", "账号长度应为10！")
            else:
                object_set = teacher.objects.filter(tno=tno)
                if object_set.count() == 0:
                    form.add_error("tno", "该账号不存在")
                else:
                    user = object_set[0]
                    if form.cleaned_data["password"] != user.tpasswd:
                        form.add_error("password", "密码错误！")
                    else:
                        request.session['tno'] = tno
                        request.session['role']='teacher'
                        url=reverse('teacherPage',args=['login'])
                        return redirect(url)
                        #return render(request, 'teacherPage.html', context)
            return render(request, 'teacherlogin.html', {'form': form})
    else:
        if request.GET.get('tno'):
            tno = request.GET.get('tno')
            form = TeaLoginForm({"tno": tno, 'password': '12345678'})
            if request.GET.get('from_url'):
                form_url = request.GET.get('from_url')
                return render(request,'teacherlogin.html',{'tno':tno,'from_url':form_url,'form':form})
        else:
            form = TeaLoginForm()
            return render(request, 'teacherlogin.html', {'form':form})


def studentlogin(request):
    form=StuLoginForm(data=request.POST)
    if request.method=='POST':
        if form.is_valid():
            sno = form.cleaned_data["sno"]
            if len(sno) != 10:
                form.add_error("sno", "学号长度为10！")
            else:
                object_set = student.objects.filter(sno=sno)
                if object_set.count() == 0:
                    form.add_error("sno", "该学号不存在")
                else:
                    user = object_set[0]
                    if form.cleaned_data["password"] != user.spasswd:
                        form.add_error("password", "密码错误！")
                    #成功登录
                    else:
                        request.session['sno'] = sno
                        request.session['role']='student'
                        url = reverse('studentPage', args=['login'])
                        return redirect(url)
            return render(request, 'studentlogin.html', {'form': form})
    else: #注册成功转到登录界面
        if request.GET.get('sno'):
            sno = request.GET.get('sno')
            form = StuLoginForm({"sno": sno, 'password': '12345678'})
            if request.GET.get('from_url'):
                from_url = request.GET.get('from_url')
                return render(request, 'studentlogin.html', {'sno': sno, 'from_url': from_url, 'form': form})
        else:
            form = StuLoginForm()
            return render(request, 'studentlogin.html', {'form': form})

def tearegister(request):
    func = None
    func = CreateTeacherView.as_view()
    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)


def sturegister(request):
    func=None
    func=CreateStudentView.as_view()
    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)



def teaOption(request,**kwargs):
    if request.method=='GET':
        operation = kwargs['operation']

        if operation == 'login':
            tno=request.session.get('tno')
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT cno, cname, ccredit, pcno
                    FROM LOGIN_course
                    WHERE tno_id = %s;''', [tno]
                )
                courses = cursor.fetchall()
            with connection.cursor() as cursor:
                cursor.execute("SELECT tname FROM LOGIN_teacher WHERE tno=%s", [tno])
                teacher_name = cursor.fetchall()
            tname = teacher_name[0][0]
            request.session['name']=tname

            context = {
                'name': tname,
                'courses': courses,
                'role': 'teacher',
                'operation': 'login'
            }
            return render(request,'teacherPage.html',context)

        if operation == '1':
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT cno, cname, ccredit, pcno,tname
                    FROM LOGIN_course,login_teacher
                    WHERE login_course.tno_id=login_teacher.tno;'''
                )
                courses = cursor.fetchall()
            context = {
                'courses':courses,
                'operation': '1',
                'name': request.session.get('name')
            }
            return render(request, 'teacherPage.html', context)

        if operation == '2':
            form = createCourse()
            context = {
                'operation': '2',
                'name': request.session.get('name'),
                'form': form
            }
            return render(request, 'teacherPage.html', context)
        if operation == '3':
            tno = request.session.get('tno')
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT cno, cname, ccredit, pcno,grading
                    FROM LOGIN_course
                    WHERE tno_id = %s;''', [tno]
                )
                courses = cursor.fetchall()
            context = {
                'name': request.session.get('name'),
                'courses': courses,
                'role': 'teacher',
                'operation': 'choose_course'
            }
            return render(request, 'teacherPage.html', context)

        if operation == '4':  #个人信息
            tno=request.session.get('tno')
            information=teacher.objects.get(tno=tno)
            context={
                'name': request.session.get('name'),
                'information': information,
                'role': 'teacher',
                'operation': 'information'
            }
            return render(request,'teacherPage.html',context)

        if operation == '5':  #删除课程
            tno = request.session.get('tno')
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT cno, cname, ccredit, pcno,grading
                    FROM LOGIN_course
                    WHERE tno_id = %s;''', [tno]
                )
                courses = cursor.fetchall()
            context = {
                'name': request.session.get('name'),
                'courses': courses,
                'role': 'teacher',
                'operation': 'delete_course'
            }
            return render(request, 'teacherPage.html', context)

        else:
            return render(request,'error.html')

    # 则是提交了创建课程的表单
    else:
        form_type=request.POST.get('form_type')
        if form_type=='createCourse':
            #print("正在试图创建课程")
            form=createCourse(request.POST)
            if form.is_valid():
                course_set = course.objects.filter().order_by("-cno")

                for i in course_set:
                    print(i.cno)
                if course_set.count() > 0:
                    last_course = course_set[0]
                    new_number = int(last_course.cno[2:5]) + 1
                    new_number = '{:0>3}'.format(new_number)
                else:
                    new_number = "001"

                new_course = form.save(commit=False)
                cno = '23' + new_number
                new_course.cno = cno
                tno = request.session.get('tno')
                teacher_instance = teacher.objects.get(tno=tno)
                new_course.tno = teacher_instance
                new_course.save()
                form.save_m2m()

                context = {
                    'operation': 'create_success',
                    'name':request.session.get('name'),
                    'cno':cno
                }
                return render(request, 'teacherPage.html',context)
            return render(request,'cal.html')

    return render(request,'error.html')




def teacherPage_view(request, operation, arg):
    if operation == 'view_students':
        #print(operation,arg)
        cno = arg
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT sno, sname, scollege, smajor,sgrade
                FROM LOGIN_student,login_sc
                WHERE login_student.sno = login_sc.sno_id 
                AND LOGIN_sc.cno_id=%s;''', [cno]
            )
            students = cursor.fetchall()


        context = {
            'operation': 'class_student',
            'students': students,
            'name': request.session.get('name')
        }
        role=request.session.get('role')
        if role=='teacher':
            return render(request, 'teacherPage.html', context)
        else:
            return render(request,'studentPage.html',context)

    if operation == 'course_grading':
        cno=arg
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT sno, sname, scollege, smajor,sgrade
                FROM LOGIN_student,login_sc
                WHERE login_student.sno = login_sc.sno_id 
                AND LOGIN_sc.cno_id=%s;''', [cno]
            )
            students = cursor.fetchall()
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT cname
                FROM LOGIN_course
                WHERE cno = %s ;''', [cno]
            )
            cname_ = cursor.fetchall()
        cname=cname_[0][0]
        context = {
            'operation': 'course_grading',
            'students': students,
            'name':request.session.get('name'),
            'cname': cname,
            'cno':cno,
        }
        request.session['students']=students
        return render(request, 'teacherPage.html', context)

    if operation == 'course_delete':
        cno=arg
        course_to_delete = course.objects.get(cno=cno)
        cname=course_to_delete.cname
        course_to_delete.delete()
        context = {
            'operation': 'delete_success',
            'name': request.session.get('name'),
            'cname': cname,
            'cno': cno
        }
        return render(request,'teacherPage.html',context)

    if operation == 'update_passwd':

        if request.method == 'POST':
            print('尝试修改密码')
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']
                teacher_ = teacher.objects.get(tno=request.session.get('tno'))
                if teacher_.tpasswd != old_password:
                    form.add_error('old_password', "原密码错误！")
                else:
                    teacher_.tpasswd = new_password
                    teacher_.save()
                    information = teacher.objects.get(tno=request.session.get('tno'))
                    context = {
                        'information': information,
                        'operation': 'changePasswd_success',
                        'name': request.session.get('name')
                    }
                    return render(request, 'teacherPage.html', context)  # 重定向到成功页面
            # 如果表单验证失败，则直接返回包含表单的页面
            context = {
                'form': form,
                'name': request.session.get('name'),
                'operation': 'change_passwd',
                'information': teacher.objects.get(tno=request.session.get('tno')),
            }
            return render(request, 'teacherPage.html', context)

        else:
          form=PasswordChangeForm()
          tno = request.session.get('tno')
          information = teacher.objects.get(tno=tno)
          context = {
              'information':information,
              'form': form,
              'name': request.session.get('name'),
              'operation': 'change_passwd'
          }
          return render(request, 'teacherPage.html', context)

    else:
        return render(request,'error.html')


def stu_updatePasswd(request, operation, arg):
    if operation == 'update_passwd':
        if request.method == 'POST':
            #print('尝试修改密码')
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']
                student_ = student.objects.get(sno=request.session.get('sno'))
                if student_.spasswd != old_password:
                    form.add_error('old_password', "原密码错误！")
                else:
                    student_.spasswd = new_password
                    student_.save()
                    information = student.objects.get(sno=request.session.get('sno'))
                    context = {
                        'information': information,
                        'operation': 'changePasswd_success',
                        'name': request.session.get('name')
                    }
                    return render(request, 'studentPage.html', context)  # 重定向到成功页面
            # 如果表单验证失败，则直接返回包含表单的页面
            context = {
                'form': form,
                'name': request.session.get('name'),
                'information':student.objects.get(sno=request.session.get('sno')),
                'operation': 'change_passwd'
            }
            return render(request, 'studentPage.html', context)

        else: #获取修改密码的表单
            form=PasswordChangeForm()
            sno = request.session.get('sno')
            information = student.objects.get(sno=sno)
            context = {
              'information':information,
              'form': form,
              'name': request.session.get('name'),
              'operation': 'change_passwd'
            }
            return render(request, 'studentPage.html', context)

    else:
        return render(request,'error.html')




def grading(request):
    cno=request.POST.get('cno')
    cname=request.POST.get('cname')
    students=request.session.get('students')
    for student in students:
        sno=student[0]
        grade=request.POST.get(sno)
        print(" grade:",grade)
        sc_instance = SC.objects.get(sno=sno, cno=cno)
        sc_instance.grade = grade
        print(sc_instance)
        sc_instance.save()

    context={
        'name':request.session.get('name'),
        'operation':'grading_success',
        'cno':cno,
        'cname':cname
    }
    course_=course.objects.get(cno=cno)
    course_.grading=True
    course_.save()
    return render(request,'teacherPage.html',context)


def stuOption(request,**kwargs):
    if request.method=='GET':
        operation = kwargs['operation']

        if operation == 'login':
            sno=request.session.get('sno')
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT cno, cname, ccredit,pcno,tname
                    FROM LOGIN_TEACHER,LOGIN_COURSE
                    WHERE LOGIN_COURSE.tno_id = LOGIN_TEACHER.tno
                    AND cno in 
                    (SELECT cno_id FROM LOGIN_SC WHERE sno_id =%s);''', [sno]
                )
                courses = cursor.fetchall()
            with connection.cursor() as cursor:
                cursor.execute("SELECT sname FROM LOGIN_student WHERE sno=%s", [sno])
                student_name = cursor.fetchall()
            sname = student_name[0][0]
            request.session['name']=sname
            context = {
                'operation':'login',
                'name': sname,
                'courses': courses,
                'role': 'student'
            }
            return render(request,'studentPage.html',context)

        if operation == '1':   #查询课程
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT cno, cname, ccredit, pcno, tname
                    FROM LOGIN_course,login_teacher
                    WHERE login_course.tno_id=login_teacher.tno;'''
                )
                courses = cursor.fetchall()
            context = {
                'courses':courses,
                'operation': '1',
                'name': request.session.get('name')
            }
            return render(request, 'studentPage.html', context)

        if operation == '2':     #选课
            sno=request.session.get('sno')
            print(sno)
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT cno, cname, ccredit, pcno, tname
                    FROM LOGIN_course,login_teacher
                    WHERE login_course.tno_id=login_teacher.tno
                    AND cno NOT IN
                    (SELECT cno_id FROM LOGIN_SC WHERE sno_id=%s);''',[sno]
                )
                courses = cursor.fetchall()
            context = {
                'courses': courses,
                'operation': '2',
                'name': request.session.get('name')
            }
            return render(request, 'studentPage.html', context)

        if operation == '3':  #查询成绩
            sno = request.session.get('sno')
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT c.cno,c.cname,c.ccredit,t.tname,c.pcno,sc.grade
                       FROM login_SC sc
                       JOIN login_course c ON sc.cno_id=c.cno
                       JOIN login_teacher t ON c.tno_id=t.tno
                       WHERE sc.sno_id = %s
                       AND sc.grade IS NOT NULL;''', [sno]
                )
                courses = cursor.fetchall()
            context = {
                'name': request.session.get('name'),
                'courses': courses,
                'operation': 'grade'
            }
            return render(request, 'studentPage.html', context)

        if operation == '4':
            sno=request.session.get('sno')
            information=student.objects.get(sno=sno)
            context={
                'name': request.session.get('name'),
                'information': information,
                'role': 'student',
                'operation': 'information'
            }
            return render(request,'studentPage.html',context)

        if operation == '5': #退课
            sno = request.session.get('sno')
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT cno, cname, ccredit,pcno,tname,grading
                    FROM LOGIN_TEACHER,LOGIN_COURSE
                    WHERE LOGIN_COURSE.tno_id = LOGIN_TEACHER.tno
                    AND cno in 
                    (SELECT cno_id FROM LOGIN_SC WHERE sno_id =%s);''', [sno]
                )
                courses = cursor.fetchall()
            context = {
                'courses': courses,
                'operation': '5',
                'name': request.session.get('name')
            }
            return render(request,'studentPage.html',context)

        else:
            return render(request,'error.html')


    return render(request,'error.html')

def select_course(request,operation,arg):
    sno=request.session.get('sno')
    cno=arg
    SC.objects.create(sno_id=sno,cno_id=cno,semester='2023')
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT cno, cname, ccredit, pcno, tname
            FROM LOGIN_course,login_teacher
            WHERE login_course.tno_id=login_teacher.tno
            AND cno NOT IN
            (SELECT cno_id FROM LOGIN_SC WHERE sno_id=%s);''', [sno]
        )
        courses = cursor.fetchall()
    context = {
        'courses': courses,
        'operation': '2_success',
        'name': request.session.get('name')
    }
    return render(request,'studentPage.html',context)


def delete_course(request,operation,arg):
    cno = arg
    sno=request.session.get('sno')
    course_to_delete = SC.objects.get(cno=cno,sno=sno)
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT cname
            FROM LOGIN_course
            WHERE cno=%s
            ;''', [cno]
        )
        course = cursor.fetchall()
    cname =course[0]
    course_to_delete.delete()
    context = {
        'operation': 'delete_success',
        'name': request.session.get('name'),
        'cname': cname,
        'cno': cno
    }
    return render(request, 'studentPage.html', context)


def course_finding(request):
    cno=request.POST.get('cno','')+'%'
    cname='%'+request.POST.get('cname','')+'%'
    credit=request.POST.get('credit')
    tname='%'+request.POST.get('teacher','')+'%'
    pcno=request.POST.get('pcno','')+'%'
    role=request.POST.get('role')

    print(cname)

    if credit == '' and pcno=='%':    #不查询先修课程的情况下
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT cno, cname, ccredit, pcno,tname
                   FROM LOGIN_course,login_teacher
                   WHERE login_course.tno_id=login_teacher.tno
                   AND cno like %s
                   AND cname like %s
                   AND tname like %s;''', [cno, cname, tname]
            )
            courses = cursor.fetchall()

    elif pcno != '%' and credit !='':  #同时查询先修课程与学分
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT cno, cname, ccredit, pcno,tname
                   FROM LOGIN_course,login_teacher
                   WHERE login_course.tno_id=login_teacher.tno
                   AND cno like %s
                   AND cname like %s
                   AND ccredit = %s
                   AND pcno like %s
                   AND tname like %s;''', [cno, cname, credit, pcno, tname]
            )
            courses = cursor.fetchall()

    elif credit!='' and pcno == '%':  #只查询学分
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT cno, cname, ccredit, pcno,tname
                   FROM LOGIN_course,login_teacher
                   WHERE login_course.tno_id=login_teacher.tno
                   AND cno like %s
                   AND cname like %s
                   AND ccredit = %s
                   AND tname like %s;''', [cno, cname, credit , tname]
            )
            courses = cursor.fetchall()

    elif pcno != '%' and credit=='':  #只查询先修课程
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT cno, cname, ccredit, pcno,tname
                   FROM LOGIN_course,login_teacher
                   WHERE login_course.tno_id=login_teacher.tno
                   AND cno like %s
                   AND cname like %s
                   AND pcno like %s
                   AND tname like %s;''', [cno, cname, pcno, tname]
            )
            courses = cursor.fetchall()

    context = {
        'courses': courses,
        'operation': '1',
        'name': request.session.get('name')
    }
    if role=='teacher':
        return render(request, 'teacherPage.html', context)
    else:
        return render(request,'studentPage.html',context)



class CreateTeacherView(CreateView):
    model = teacher
    form_class = TeaRegisterForm
    template_name = "tearegister.html"
    success_url = "teacherlogin"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = None
            return self.form_invalid(form)

    def form_valid(self, form):
        college=form.cleaned_data['tcollege']
        if college=='计算机学院':
            co_no=1
        elif college=='航天学院':
            co_no=2
        elif college=='自动化学院':
            co_no=3
        else:
            co_no=4
        # 把非三位数的院系号转换为以0填充的三位字符串，如1转换为'001'
        co_no = '{:0>3}'.format(co_no)
        teacher_set = teacher.objects.filter(tcollege=college).order_by("-number")
        if teacher_set.count() > 0:
            last_teacher = teacher_set[0]
            new_number = int(last_teacher.number) + 1
            new_number = '{:0>7}'.format(new_number)
        else:
            new_number = "0000001"

        # Create, but don't save the new teacher instance.
        new_teacher = form.save(commit=False)
        # Modify the teacher
        tno=co_no+new_number
        new_teacher.tno = tno
        new_teacher.number=new_number
        # Save the new instance.
        new_teacher.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_teacher

        tno = co_no + new_number
        base_url = reverse(self.get_success_url())
        return redirect(base_url + '?tno=%s&from_url=%s' % (tno,'register'))


class CreateStudentView(CreateView):
    model = student
    form_class = StuRegisterForm
    template_name = "sturegister.html"
    success_url = "studentlogin"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = None
            return self.form_invalid(form)

    def form_valid(self, form):
        college=form.cleaned_data['scollege']
        if college=='计算机学院':
            co_no=1
        elif college=='航天学院':
            co_no=2
        elif college=='自动化学院':
            co_no=3
        else:
            co_no=4
        # 把非三位数的院系号转换为以0填充的三位字符串，如1转换为'001'
        grade=form.cleaned_data['sgrade']
        co_no = '{:0>2}'.format(co_no)
        student_set = student.objects.filter(scollege=college).order_by("-number")
        if student_set.count() > 0:
            last_student = student_set[0]
            new_number = int(last_student.number) + 1
            new_number = '{:0>4}'.format(new_number)
        else:
            new_number = "0001"

        # Create, but don't save the new student instance.
        new_student = form.save(commit=False)
        # Modify the student
        sno=grade+co_no+new_number
        new_student.sno = sno
        new_student.number=new_number
        # Save the new instance.
        new_student.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_student

        sno=grade+co_no+new_number
        base_url = reverse(self.get_success_url())
        return redirect(base_url + '?sno=%s&from_url=%s' % (sno,'register'))


def error(request):
    return render(request,'error.html')

