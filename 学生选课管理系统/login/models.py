from django.db import models

# Create your models here.


class student(models.Model):
    sno=models.CharField(max_length=20,blank=False,primary_key=True,verbose_name="学号")
    sname=models.CharField(max_length=40,blank=False,verbose_name="姓名")
    sbirthdate=models.DateField(verbose_name="出生日期")
    sex_choice = [
        ("m", "男"),
        ("f", "女")
    ]
    college_choice=[('计算机学院','计算机学院'),
                    ('自动化学院','自动化学院'),
                    ('航天学院','航天学院'),
                    ('数学学院','数学学院')
                    ]
    ssex = models.CharField(max_length=2, choices=sex_choice, blank=False,default='男',verbose_name="性别")  # 性别
    scollege=models.CharField(max_length=40,blank=False,choices=college_choice,verbose_name="学院")
    number = models.CharField(max_length=7, verbose_name="院内编号",default='0000000')
    sgrade=models.CharField(max_length=4,verbose_name="年级")
    smajor=models.CharField(max_length=60,blank=False,verbose_name="专业")
    spasswd = models.CharField(max_length=100, blank=False,verbose_name="密码")


class teacher(models.Model):
    tno=models.CharField(max_length=20,primary_key=True,verbose_name="教职工号")
    tname=models.CharField(max_length=40,blank=False,verbose_name="姓名")
    tbirthdate=models.DateField(verbose_name="出生日期")
    sex_choice = [
        ("m", "男"),
        ("f", "女")
    ]
    college_choice = [('计算机学院', '计算机学院'),
                      ('自动化学院', '自动化学院'),
                      ('航天学院', '航天学院'),
                      ('数学学院', '数学学院')
                      ]
    tsex = models.CharField(max_length=2, choices=sex_choice, blank=False,default='男',verbose_name="性别")  # 性别
    tcollege=models.CharField(max_length=40,blank=False,choices=college_choice,verbose_name="学院")
    number = models.CharField(max_length=7, verbose_name="院内编号",default='0000000')
    tpasswd=models.CharField(max_length=100,blank=False,verbose_name="密码")



class course(models.Model):
    cno=models.CharField(max_length=5,primary_key=True,verbose_name="课程号") #系统分配
    cname=models.CharField(max_length=60,blank=False,verbose_name="课程名")   #教师填写
    ccredit=models.FloatField(verbose_name="学分",blank=False)                          #教师填写
    pcno=models.CharField(max_length=20,verbose_name="先修课程",null=True,blank=True,help_text="如果有先修课程，请填写对应先修课程课程号，否则留空")              #教师填写
    tno = models.ForeignKey('login.teacher',on_delete=models.CASCADE,to_field='tno',verbose_name="教师")      #系统自动获取
    grading = models.BooleanField(verbose_name="是否打分",default=False)







class SC(models.Model):
    sno=models.ForeignKey('login.student',on_delete=models.CASCADE,to_field='sno',related_name='students',verbose_name="课程号")
    cno=models.ForeignKey('course',on_delete=models.CASCADE,to_field='cno',verbose_name="学号")
    grade=models.IntegerField(verbose_name="成绩",null=True)
    semester=models.CharField(max_length=5,verbose_name="学期")