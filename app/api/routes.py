from flask import Blueprint, request, jsonify, current_app, send_file, session
from app.models.models import db, Notice, Image, JrCollegeNotice
from app.utils.helpers import allowed_file, generate_unique_filename
from werkzeug.security import safe_join
import os
import platform
from werkzeug.utils import secure_filename
from datetime import datetime, timezone, timedelta
import logging
from logging.handlers import RotatingFileHandler

log_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_directory, exist_ok=True)
uptime_log_file = os.path.join(log_directory, 'uptime.log')

uptime_logger = logging.getLogger('uptime_logger')
uptime_logger.setLevel(logging.INFO)
handler = RotatingFileHandler(uptime_log_file, maxBytes=10485760, backupCount=5)  # 10MB per file, keep 5 backups
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
uptime_logger.addHandler(handler)

IST_OFFSET = timezone(timedelta(hours=5, minutes=30))
SERVER_START_TIME = datetime.now(IST_OFFSET)

uptime_logger.info(f"Server started at {SERVER_START_TIME.isoformat()}")

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/system-info', methods=['GET'])
def get_system_info():
    """
    Get system information including uptime
    ---
    responses:
      200:
        description: System information including uptime
    """
    current_time = datetime.now(IST_OFFSET)
    uptime = current_time - SERVER_START_TIME
    
    uptime_seconds = uptime.total_seconds()
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_str = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
    
    uptime_logger.info(f"Server uptime: {uptime_str} | Start: {SERVER_START_TIME.isoformat()} | Current: {current_time.isoformat()}")
    
    system_info = {
        "server_uptime": uptime_str,
        "server_start_time": SERVER_START_TIME.isoformat(),
        "current_time": current_time.isoformat(),
        "system": platform.system(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "platform_info": platform.platform(),
        "processor": platform.processor()
    }
    
    return jsonify({
        "status": "success",
        "data": system_info
    })

@api_bp.route('/notices', methods=['GET'])
def get_notices():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)
    notice_type = request.args.get('type')
    
    query = Notice.query
    
    if notice_type:
        query = query.filter_by(notice_type=notice_type)
    
    pagination = query.order_by(Notice.date_uploaded.desc()).paginate(page=page, per_page=per_page)
    notices = pagination.items
    
    notice_list = []
    for notice in notices:
        notice_data = {
            'id': notice.id,
            'title': notice.title,
            'url': notice.url,
            'date_uploaded': notice.date_uploaded.isoformat() if notice.date_uploaded else None,
            'notice_type': notice.notice_type
        }
        notice_list.append(notice_data)
    
    return jsonify({
        'notices': notice_list,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@api_bp.route('/notices/general', methods=['GET'])
def get_general_notices():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)
    date_filter = request.args.get('date')
    month_filter = request.args.get('month')
    text_filter = request.args.get('text')
    
    query = Notice.query.filter_by(notice_type='general')
    
    # Apply filters
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Notice.date_uploaded) == filter_date)
        except ValueError:
            pass
    
    if month_filter:
        try:
            month = int(month_filter)
            if 1 <= month <= 12:
                query = query.filter(db.func.extract('month', Notice.date_uploaded) == month)
        except ValueError:
            pass
    
    if text_filter:
        query = query.filter(Notice.title.contains(text_filter))
    
    pagination = query.order_by(Notice.date_uploaded.desc()).paginate(page=page, per_page=per_page)
    notices = pagination.items
    
    notice_list = []
    for notice in notices:
        notice_data = {
            'id': notice.id,
            'title': notice.title,
            'url': notice.url,
            'date_uploaded': notice.date_uploaded.isoformat() if notice.date_uploaded else None,
            'notice_type': notice.notice_type
        }
        notice_list.append(notice_data)
    
    return jsonify({
        'notices': notice_list,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@api_bp.route('/notices/exam', methods=['GET'])
def get_exam_notices():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)
    date_filter = request.args.get('date')
    month_filter = request.args.get('month')
    text_filter = request.args.get('text')
    
    query = Notice.query.filter_by(notice_type='exam')
    
    # Apply filters
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Notice.date_uploaded) == filter_date)
        except ValueError:
            pass
    
    if month_filter:
        try:
            month = int(month_filter)
            if 1 <= month <= 12:
                query = query.filter(db.func.extract('month', Notice.date_uploaded) == month)
        except ValueError:
            pass
    
    if text_filter:
        query = query.filter(Notice.title.contains(text_filter))
    
    pagination = query.order_by(Notice.date_uploaded.desc()).paginate(page=page, per_page=per_page)
    notices = pagination.items
    
    notice_list = []
    for notice in notices:
        notice_data = {
            'id': notice.id,
            'title': notice.title,
            'url': notice.url,
            'date_uploaded': notice.date_uploaded.isoformat() if notice.date_uploaded else None,
            'notice_type': notice.notice_type
        }
        notice_list.append(notice_data)
    
    return jsonify({
        'notices': notice_list,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@api_bp.route('/notices', methods=['POST'])
def add_notice():
    """
    Add a new notice
    ---
    parameters:
      - name: file
        in: formData
        type: file
        description: PDF file to upload
      - name: title
        in: formData
        type: string
        description: Notice title
      - name: notice_type
        in: formData
        type: string
        description: Notice type (general or exam)
      - name: url
        in: formData
        type: string
        description: URL (if no file is uploaded)
    responses:
      201:
        description: Notice created successfully
      400:
        description: Bad request
      401:
        description: Unauthorized
      500:
        description: Server error
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized', 'message': 'Login required'}), 401
        
    try:
        has_file = 'file' in request.files and request.files['file'] and request.files['file'].filename
        
        url_in_form = 'url' in request.form and request.form['url'].strip()
        
        notice_type = request.form.get('notice_type', 'general')
        if notice_type not in ['general', 'exam']:
            notice_type = 'general'  # Default to general if invalid type
        
        if not has_file and not url_in_form and request.content_type != 'application/json':
            return jsonify({'error': 'Missing data', 'message': 'Either file upload or URL is required'}), 400
        
        if has_file:
            file = request.files['file']
            if allowed_file(file.filename):
                filename = generate_unique_filename(file.filename)
                
                filepath = safe_join(current_app.config['UPLOAD_FOLDER'], filename)
                if not filepath:
                    return jsonify({'error': 'Invalid file path', 'message': 'Security issue with file path'}), 400
                    
                file.save(filepath)
                title = request.form.get('title', filename)
                new_notice = Notice(title=title, url=f'/uploads/{filename}', filename=filename, notice_type=notice_type)
                db.session.add(new_notice)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Notice added successfully', 'notice': new_notice.to_dict()}), 201
            return jsonify({'error': 'Invalid file', 'message': 'Invalid file format'}), 400
        
        if url_in_form:
            title = request.form.get('title', '')
            url = request.form['url']
            
            if not url.startswith(('http://', 'https://', '/uploads/')):
                return jsonify({'error': 'Invalid URL', 'message': 'Invalid URL format'}), 400
                
            new_notice = Notice(title=title, url=url, notice_type=notice_type)
            db.session.add(new_notice)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Notice added successfully', 'notice': new_notice.to_dict()}), 201
            
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Missing data', 'message': 'Title required'}), 400
        
        if 'url' not in data or not data['url']:
            return jsonify({'error': 'Missing data', 'message': 'URL required when not uploading a file'}), 400
            
        if not data['url'].startswith(('http://', 'https://', '/uploads/')):
            return jsonify({'error': 'Invalid URL', 'message': 'Invalid URL format'}), 400
            
        notice_type = data.get('notice_type', 'general')
        if notice_type not in ['general', 'exam']:
            notice_type = 'general'  # Default to general if invalid type
            
        new_notice = Notice(title=data['title'], url=data['url'], notice_type=notice_type)
        db.session.add(new_notice)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Notice added successfully', 'notice': new_notice.to_dict()}), 201
        
    except ValueError as e:
        return jsonify({'error': 'Validation error', 'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api_bp.route('/notices/<int:notice_id>', methods=['DELETE'])
def delete_notice(notice_id):
    """
    Delete a notice
    ---
    parameters:
      - name: notice_id
        in: path
        type: integer
        required: true
        description: Notice ID to delete
    responses:
      200:
        description: Notice deleted successfully
      401:
        description: Unauthorized
      404:
        description: Notice not found
      500:
        description: Server error
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized', 'message': 'Login required'}), 401
        
    try:
        notice = Notice.query.get_or_404(notice_id)
        
        if notice.filename:
            filepath = safe_join(current_app.config['UPLOAD_FOLDER'], notice.filename)
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                
        db.session.delete(notice)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Notice deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded files
    ---
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: File name to retrieve
    responses:
      200:
        description: File content
      400:
        description: Invalid filename
      404:
        description: File not found
      500:
        description: Error accessing file
    """
    filename = secure_filename(filename)
    if not filename:
        return jsonify({'error': 'Invalid filename', 'message': 'Invalid filename'}), 400
        
    try:
        filepath = safe_join(current_app.config['UPLOAD_FOLDER'], filename)
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found', 'message': 'File not found'}), 404
            
        return send_file(filepath)
    except Exception as e:
        return jsonify({'error': 'File access error', 'message': str(e)}), 500

@api_bp.route('/images', methods=['POST'])
def add_image():
    """
    Add a new image
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Image file to upload
      - name: title
        in: formData
        type: string
        required: true
        description: Image title
      - name: category
        in: formData
        type: string
        required: true
        description: Image category (e.g., cultural, sports)
      - name: description
        in: formData
        type: string
        description: Image description (optional)
    responses:
      201:
        description: Image created successfully
      400:
        description: Bad request
      401:
        description: Unauthorized
      500:
        description: Server error
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized', 'message': 'Login required'}), 401
        
    try:
        if 'file' not in request.files or not request.files['file'] or not request.files['file'].filename:
            return jsonify({'error': 'Missing file', 'message': 'Image file is required'}), 400
            
        file = request.files['file']
        if not allowed_file(file.filename, ['jpg', 'jpeg', 'png', 'gif']):
            return jsonify({'error': 'Invalid file', 'message': 'Invalid image format. Allowed formats: jpg, jpeg, png, gif'}), 400
            
        title = request.form.get('title', '')
        if not title:
            return jsonify({'error': 'Missing data', 'message': 'Title is required'}), 400
            
        category = request.form.get('category', 'general')
        description = request.form.get('description', '')
        
        filename = generate_unique_filename(file.filename)
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images', category)
        
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = safe_join(upload_folder, filename)
        if not filepath:
            return jsonify({'error': 'Invalid file path', 'message': 'Security issue with file path'}), 400
            
        file.save(filepath)
        
        new_image = Image(
            title=title,
            filename=f"{category}/{filename}",
            category=category,
            description=description
        )
        db.session.add(new_image)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Image added successfully', 
            'image': new_image.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Validation error', 'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api_bp.route('/images', methods=['GET'])
def get_images():
    """
    Get paginated images with optional category filter
    ---
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number
      - name: per_page
        in: query
        type: integer
        default: 12
        description: Items per page
      - name: category
        in: query
        type: string
        description: Filter by category
    responses:
      200:
        description: A list of images
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category = request.args.get('category')
    
    query = Image.query
    
    if category:
        query = query.filter(Image.category == category)
    
    query = query.order_by(Image.date_uploaded.desc())
    
    pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    images = pagination.items
    
    return jsonify({
        'images': [image.to_dict() for image in images],
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'page': page,
        'pages': pagination.pages,
        'total': pagination.total
    })

@api_bp.route('/images/categories', methods=['GET'])
def get_image_categories():
    """
    Get all available image categories
    ---
    responses:
      200:
        description: A list of image categories
    """
    categories = db.session.query(Image.category).distinct().all()
    return jsonify({
        'categories': [category[0] for category in categories]
    })

@api_bp.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    """
    Delete an image
    ---
    parameters:
      - name: image_id
        in: path
        type: integer
        required: true
        description: Image ID to delete
    responses:
      200:
        description: Image deleted successfully
      401:
        description: Unauthorized
      404:
        description: Image not found
      500:
        description: Server error
    """
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized', 'message': 'Login required'}), 401
        
    try:
        image = Image.query.get_or_404(image_id)
        
        filepath = safe_join(current_app.config['UPLOAD_FOLDER'], 'images', image.filename)
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            
        db.session.delete(image)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Image deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api_bp.route('/uploads/images/<path:filename>')
def uploaded_image(filename):
    """
    Serve uploaded image files
    ---
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: Image filename to retrieve (can include category path)
    responses:
      200:
        description: Image file
      400:
        description: Invalid filename
      404:
        description: File not found
      500:
        description: Error accessing file
    """
    if '..' in filename or filename.startswith('/'):
        return jsonify({'error': 'Invalid filename', 'message': 'Invalid filename'}), 400
        
    try:
        path_parts = filename.split('/')
        if len(path_parts) > 1:
            filepath = safe_join(current_app.config['UPLOAD_FOLDER'], 'images', filename)
        else:
            filepath = safe_join(current_app.config['UPLOAD_FOLDER'], 'images', 'general', filename)
            
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found', 'message': 'Image not found'}), 404
            
        return send_file(filepath)
    except Exception as e:
        return jsonify({'error': 'File access error', 'message': str(e)}), 500

# Jr College Notice API Endpoints
@api_bp.route('/jr-college/notices', methods=['GET'])
def get_jr_college_notices():
    """Get Jr College notices with pagination and filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)
    notice_type = request.args.get('type')
    priority = request.args.get('priority')
    is_active = request.args.get('active')
    
    query = JrCollegeNotice.query
    
    if notice_type:
        query = query.filter(JrCollegeNotice.notice_type == notice_type)
    
    if priority:
        query = query.filter(JrCollegeNotice.priority == priority)
    
    if is_active is not None:
        active_filter = is_active.lower() == 'true'
        query = query.filter(JrCollegeNotice.is_active == active_filter)
    
    pagination = query.order_by(JrCollegeNotice.date_uploaded.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    notices = pagination.items
    
    return jsonify({
        'success': True,
        'notices': [notice.to_dict() for notice in notices],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    })

@api_bp.route('/jr-college/notices', methods=['POST'])
def create_jr_college_notice():
    """Create a new Jr College notice"""
    try:
        # Get form data
        title = request.form.get('title')
        notice_type = request.form.get('notice_type', 'general')
        priority = request.form.get('priority', 'normal')
        url = request.form.get('url')
        
        if not title:
            return jsonify({'success': False, 'message': 'Title is required'}), 400
        
        # Handle file upload
        uploaded_file = request.files.get('file')
        final_url = url
        filename = None
        
        if uploaded_file and uploaded_file.filename:
            # Define allowed extensions for Jr College notices
            allowed_extensions = ['pdf', 'doc', 'docx']
            if not allowed_file(uploaded_file.filename, allowed_extensions):
                return jsonify({'success': False, 'message': 'Invalid file type. Only PDF, DOC, and DOCX files are allowed.'}), 400
            
            # Create secure filename
            filename = secure_filename(uploaded_file.filename)
            upload_folder = os.path.join(current_app.static_folder, 'docs', 'jr-college')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_folder, filename)
            uploaded_file.save(file_path)
            
            # Create URL for the file
            final_url = f"/static/docs/jr-college/{filename}"
        
        if not final_url:
            return jsonify({'success': False, 'message': 'Either a file or URL must be provided'}), 400
        
        # Create new notice
        notice = JrCollegeNotice(
            title=title,
            url=final_url,
            filename=filename,
            notice_type=notice_type,
            priority=priority
        )
        notice.is_active = True
        
        db.session.add(notice)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Notice added successfully',
            'notice': notice.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating Jr College notice: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while creating the notice'}), 500

@api_bp.route('/jr-college/notices/<int:notice_id>', methods=['DELETE'])
def delete_jr_college_notice(notice_id):
    """Delete a Jr College notice"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized', 'message': 'Login required'}), 401
        
    try:
        notice = JrCollegeNotice.query.get_or_404(notice_id)
        
        if notice.filename:
            from werkzeug.security import safe_join
            filepath = safe_join(current_app.static_folder, 'docs', 'jr-college', notice.filename)
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                
        db.session.delete(notice)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Notice deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@api_bp.route('/jr-college/stats', methods=['GET'])
def get_jr_college_stats():
    """Get Jr College notice statistics"""
    try:
        total_notices = JrCollegeNotice.query.count()
        active_notices = JrCollegeNotice.query.filter(JrCollegeNotice.is_active == True).count()
        high_priority = JrCollegeNotice.query.filter(JrCollegeNotice.priority == 'high').count()
        
        # Count by notice type
        general_count = JrCollegeNotice.query.filter(JrCollegeNotice.notice_type == 'general').count()
        admission_count = JrCollegeNotice.query.filter(JrCollegeNotice.notice_type == 'admission').count()
        exam_count = JrCollegeNotice.query.filter(JrCollegeNotice.notice_type == 'exam').count()
        event_count = JrCollegeNotice.query.filter(JrCollegeNotice.notice_type == 'event').count()
        
        # This month count
        from datetime import datetime
        this_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        this_month_count = JrCollegeNotice.query.filter(JrCollegeNotice.date_uploaded >= this_month_start).count()
        
        return jsonify({
            'total_notices': total_notices,
            'active_notices': active_notices,
            'high_priority': high_priority,
            'this_month': this_month_count,
            'by_type': {
                'general': general_count,
                'admission': admission_count,
                'exam': exam_count,
                'event': event_count
            }
        })
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500
