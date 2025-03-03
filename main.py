import json
import csv

def extract_custom_attributes(file_path):
    
    with open(file_path, 'r') as p:
        data = json.load(p)
    
    variants = data.get("allVariants", [])

    attributesRaw = variants[0].get("attributesRaw", [])

    for attr in attributesRaw:
            if attr.get("name") == "custom_attributes":
                custom_attr = attr.get("value")
                break
     
    products = []    

    for key, json_str in custom_attr.items():
        
        try:
            parsed_value = json.loads(json_str)
            extracted = {
                "allergens": parsed_value.get("allergens", {}).get("value"),
                "sku": parsed_value.get("sku", {}).get("value"),
                "vegan": parsed_value.get("vegan", {}).get("value"),
                "kosher": parsed_value.get("kosher", {}).get("value"),
                "organic": parsed_value.get("organic", {}).get("value"),
                "vegetarian": parsed_value.get("vegetarian", {}).get("value"),
                "gluten_free": parsed_value.get("gluten_free", {}).get("value"),
                "lactose_free": parsed_value.get("lactose_free", {}).get("value"),
                "package_quantity": parsed_value.get("package_quantity", {}).get("value"),
                "unit_size": parsed_value.get("unit_size", {}).get("value"),
                "net_weight": parsed_value.get("net_weight", {}).get("value")
            }
            products.append(extracted)
        except json.JSONDecodeError as e:
            print("Error al parsear:", e)

    return products



def json_list_to_csv(json_list, csv_file):

    headers = [
        'allergens',
        'sku',
        'vegan',
        'kosher',
        'organic',
        'vegetarian',
        'gluten_free',
        'lactose_free',
        'package_quantity',
        'unit_size',
        'net_weight'
    ]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for item in json_list:
            
            allergens_list = item.get('allergens', [])
            allergens_names = ', '.join([al.get('name', '') for al in allergens_list])
            
            row = {
                'allergens': allergens_names,
                'sku': item.get('sku'),
                'vegan': item.get('vegan'),
                'kosher': item.get('kosher'),
                'organic': item.get('organic'),
                'vegetarian': item.get('vegetarian'),
                'gluten_free': item.get('gluten_free'),
                'lactose_free': item.get('lactose_free'),
                'package_quantity': item.get('package_quantity'),
                'unit_size': item.get('unit_size'),
                'net_weight': item.get('net_weight')
            }
            writer.writerow(row)



if __name__ == "__main__":
    file_path = "product.json" 
    try:
        custom_attrs = extract_custom_attributes(file_path)
        output_csv = 'output.csv'
        json_list_to_csv(custom_attrs, output_csv)
        print(f"Archivo CSV '{output_csv}' creado exitosamente.")

    except Exception as e:
        print("Error:", e)




