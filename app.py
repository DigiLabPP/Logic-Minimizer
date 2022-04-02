from flask import Flask , render_template, request , url_for
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/logicmin')
def logic_min():
    return render_template('minimizer.html',message="",disp="none")


@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')


# // APIs

@app.route('/minimizer',methods=["POST"])
def minimizer():
    import user_defined_code.logicmin as lm
    var = tuple(request.form.get("var").split())
    num = request.form.get("num")
    minterms = request.form.get("minterms").split()
    dontcares = request.form.get("dontcares").split()

    if(len(var)==0 or len(minterms)==0 or len(dontcares)==0 or num==""):
        message = "Fill the form properly!"
        visib = "block"
        return render_template("minimizer.html",message=message,disp=visib)
    else:
        num = int(num)

    if(len(dontcares)>(2**num) or len(minterms)>(2**num)):
        message = "Number of minterms greater than total number of terms!"
        visib = "block"
        return render_template("minimizer.html",message=message,disp=visib)

    if(len(var)<num):
        message = "Number of Variables names provided is less!"
        visib = "block"
        return render_template("minimizer.html",message=message,disp=visib)

    for i in range(len(minterms)):
        minterms[i] = int(minterms[i])

    pr = 0
    for i in range(len(dontcares)):
        dontcares[i] = int(dontcares[i])
        if(dontcares[i] in minterms):
            pr =1
            break

    if(pr==1):
        message = "Don't care present in Min Term!"
        visib = "block"
        return render_template("minimizer.html",message=message,disp=visib)
    
    print(var,type(var))
    print(num,type(num))
    print(minterms,type(minterms))
    print(dontcares,type(dontcares))
    sop,pos = lm.simplify(minterms,dontcares,lm.Minimize(minterms,dontcares,num),num,var)
    print(sop,pos)
    return render_template("mini_result.html",sop=sop,pos=pos)

if __name__ == "__main__":
    app.run(debug=False)