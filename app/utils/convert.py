def serialize_data(data):
  converted_data = []
  for item in data:
    converted_item = []
    
    for value in item:
      if value is not None:
        converted_item.append(str(value))
      else:
        converted_item.append('')

    # # Convert each element in the tuple to string versi shorthand
    # converted_item = [str(value) if value is not None else '' for value in item]

    converted_data.append(tuple(converted_item))  # Append as a tuple
  return converted_data