from flask import Blueprint, request, session, redirect, url_for, render_template, current_app, flash, send_from_directory, jsonify, send_file
import os

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@frontend_bp.route('/student/<string:subpath>', methods=['GET'])
def student(subpath):
    try:
        return render_template(f'student/{subpath}.html')
    except:
        return render_template('404.html')
    
@frontend_bp.route('/about/<string:subpath>', methods=['GET'])
def about(subpath):
    try:
        return render_template(f'about/{subpath}.html')
    except:
        return render_template('404.html')

@frontend_bp.route('/academics/<string:subpath>', methods=['GET'])
def academics(subpath):
    try:
        return render_template(f'academics/{subpath}.html')
    except:
        return render_template('404.html')

@frontend_bp.route('/admin/jr-college', methods=['GET', 'POST'])
def jr_college_admin():
    """Jr College Admin Panel with password protection"""
    try:
        # Simple password check
        if request.method == 'POST':
            password = request.form.get('password')
            if password == 'jrcollege2024':  # Simple password
                session['jr_college_admin'] = True
                return redirect(url_for('frontend.jr_college_admin'))
            else:
                flash('Invalid password!', 'error')
        
        # Check if admin is logged in
        if not session.get('jr_college_admin'):
            return render_template('admin/jr_college_login.html')
        
        return render_template('admin/jr_college_admin.html')
    except Exception as e:
        current_app.logger.error(f"Error in jr_college_admin route: {str(e)}")
        return render_template('404.html')

@frontend_bp.route('/admin/jr-college/logout', methods=['GET'])
def jr_college_admin_logout():
    """Logout from Jr College admin"""
    session.pop('jr_college_admin', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('frontend.jr_college_admin'))

@frontend_bp.route('/admin/jr-college/upload-notice', methods=['POST'])
def upload_jr_college_notice():
    """Handle Jr College notice upload"""
    try:
        from app.models.models import JrCollegeNotice, db
        from werkzeug.utils import secure_filename
        import os
        
        title = request.form.get('title')
        notice_type = request.form.get('notice_type')
        priority = request.form.get('priority', 'normal')
        is_active = request.form.get('is_active') == 'true'
        
        if not title or not notice_type:
            flash('Title and notice type are required!', 'error')
            return redirect(url_for('frontend.jr_college_admin'))
        
        file = request.files.get('notice_file')
        if not file or file.filename == '':
            flash('Please select a file to upload!', 'error')
            return redirect(url_for('frontend.jr_college_admin'))
        
        # Validate file type
        allowed_extensions = {'pdf', 'doc', 'docx'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            flash('Only PDF, DOC, and DOCX files are allowed!', 'error')
            return redirect(url_for('frontend.jr_college_admin'))
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.static_folder, 'docs', 'jr-college')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Create URL for the file
        file_url = url_for('static', filename=f'docs/jr-college/{filename}')
        
        # Save to database
        notice = JrCollegeNotice(
            title=title,
            url=file_url,
            filename=filename,
            notice_type=notice_type,
            priority=priority
        )
        notice.is_active = is_active
        
        db.session.add(notice)
        db.session.commit()
        
        flash('Notice uploaded successfully!', 'success')
        return redirect(url_for('frontend.jr_college_admin'))
        
    except Exception as e:
        current_app.logger.error(f"Error uploading notice: {str(e)}")
        flash('Error uploading notice. Please try again.', 'error')
        return redirect(url_for('frontend.jr_college_admin'))

@frontend_bp.route('/library/<string:subpath>', methods=['GET'])
def library(subpath):
    try:
        return render_template(f'library/{subpath}.html')
    except:
        return render_template('404.html')

@frontend_bp.route('/extension/<string:subpath>', methods=['GET'])
def extension(subpath):
    try:
        return render_template(f'extension/{subpath}.html')
    except:
        return render_template('404.html')
        
@frontend_bp.route('/examination/<string:subpath>', methods=['GET'])
def examination(subpath):
    try:
        if subpath == 'notices':
            import requests
            from flask import current_app
            
            api_url = f"{request.url_root}api/notices/exam"
            response = requests.get(api_url, verify=False)
            notices = []
            
            if response.status_code == 200:
                data = response.json()
                notices = data.get('notices', [])
            
            return render_template(f'examination/{subpath}.html', notices=notices)
        else:
            return render_template(f'examination/{subpath}.html')
    except Exception as e:
        current_app.logger.error(f"Error in examination route: {str(e)}")
        return render_template('404.html')

@frontend_bp.route('/feedback/<string:subpath>', methods=['GET'])
def feedback(subpath):
    try:
        return render_template(f'feedback/{subpath}.html')
    except:
        return render_template('404.html')

@frontend_bp.route('/more/<string:subpath>', methods=['GET'])
def more(subpath):
    try:
        return render_template(f'more/{subpath}.html')
    except:
        return render_template('404.html')
    
@frontend_bp.route('/research/<string:subpath>', methods=['GET'])
def research(subpath):
    try:
        return render_template(f'research/{subpath}.html')
    except:
        return render_template('404.html')

@frontend_bp.route('/<string:subpath>', methods=['GET'])
def facu(subpath):
    try:
        return render_template(f'facu/{subpath}.html')
    except:
        return render_template('404.html')

@frontend_bp.route('/naac', methods=['GET'])
def naac():
    return render_template('facu/naac.html', active_section="naac-dvv")

@frontend_bp.route('/naac/dvv', methods=['GET'])
def naac_dvv():
    return render_template('facu/naac.html', active_section="naac-dvv")

@frontend_bp.route('/naac/appeal', methods=['GET'])
def naac_appeal():
    return render_template('facu/naac.html', active_section="naac-appeal")

@frontend_bp.route('/naac/iqac', methods=['GET'])
def naac_iqac():
    return render_template('facu/naac.html', active_section="iqac")

@frontend_bp.route('/naac/strategic-plan', methods=['GET'])
def naac_strategic_plan():
    return render_template('facu/naac.html', active_section="strategic-plan")

@frontend_bp.route('/naac/aqar', methods=['GET'])
def naac_aqar():
    return render_template('facu/naac.html', active_section="aqar")

@frontend_bp.route('/naac/iiqa', methods=['GET'])
def naac_iiqa():
    return render_template('facu/naac.html', active_section="iiqa")

@frontend_bp.route('/naac/ssr', methods=['GET'])
def naac_ssr():
    return render_template('facu/naac.html', active_section="ssr")

@frontend_bp.route('/naac/criteria-docs', methods=['GET'])
def naac_criteria_docs():
    return render_template('facu/naac.html', active_section="criteria-docs")

@frontend_bp.route('/naac/institutional', methods=['GET'])
def naac_institutional():
    return render_template('facu/naac.html', active_section="institutional")

@frontend_bp.route('/gandhi-center', methods=['GET'])
def gandhi_center():
    return render_template('about/gandhi-center.html')

@frontend_bp.route('/purvanchal-trust', methods=['GET'])
def purvanchal_trust():
    return render_template('/purvanchal-trust.html')

@frontend_bp.route('/docs/<path:filepath>', methods=['GET'])
def serve_docs(filepath):
    import os
    from flask import abort, current_app
    import urllib.parse

    # URL decode the filepath to handle special characters
    filepath = urllib.parse.unquote(filepath)
    docs_dir = os.path.join('docs')
    file_path = os.path.join(docs_dir, filepath)
        
    try:
        # Use safe_join to prevent directory traversal attacks
        from werkzeug.utils import safe_join
        safe_path = safe_join(docs_dir, filepath)
        return send_file(safe_path)
    except Exception as e:
        return jsonify({"Not Found"}), 404  