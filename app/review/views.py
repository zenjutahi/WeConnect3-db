from flask import request, jsonify

from . import review
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Business, Review
from app.view_helpers import token_generator
from app.utils import check_blank_key, validate_buss_data_null, require_json


@review.route('/<int:business_id>/reviews', methods=['GET', 'POST'])
@require_json
@jwt_required
def make_businessreview(business_id):
    current_user = get_jwt_identity()
    business_to_review = Business.query.filter_by(id=business_id).first()
    print(business_to_review)
    if request.method == 'POST':
        if not business_to_review:
            return jsonify(
                {'message': 'You can only review an existing business'}), 409
        try:
            required_fields = ['value', 'comments']
            data = check_blank_key(request.get_json(), required_fields)
        except AssertionError as err:
            msg = err.args[0]
            return jsonify({"message": msg}), 422
        value = validate_buss_data_null(data['value'])
        comments = validate_buss_data_null(data['comments'])
        if not value or not comments:
            return jsonify(
                {'message': 'You have to enter a review value and comment'}), 400
        if current_user == business_to_review.user_id:
            return jsonify(
                {'message': 'You can not review your own business'}), 403
        new_review = Review(
            value=value,
            comments=comments,
            business_id=business_id,
            user_id=current_user)
        new_review.save()
        display_review = Review.query.filter_by(id=new_review.id).first()
        info = display_review.accesible()

        return jsonify({'message': 'You have successfully created a review',
                        'Review': info}), 201

    # retreving a single business's reviews
    if not business_to_review:
        return jsonify(
            {'message': 'Enter an existing business'}), 409
    all_reviews = Review.get_all(Review)
    # using lambda and map
    def func(review): return review.accesible(
    ) if review.business_id == business_id else False
    all_reviews = filter(lambda item: item and True, map(func, all_reviews))
    data = list(all_reviews)
    if len(data) == 0:
        return jsonify({'message': 'No review for this business'}), 201

    return jsonify({'message': 'Reviews for business with id {} are :'.format(
        business_id), 'reviews ': data}), 201
