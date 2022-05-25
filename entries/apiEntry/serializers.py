from datetime import datetime
from rest_framework import serializers
from entries.models import Entry

class EntrySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    concept = serializers.CharField()
    amount = serializers.FloatField()
    datetime = serializers.DateTimeField()
    
    
    def create(self,validated_data):
        #pre: validated data
        #post: create new Entry with the validated_date,
        return self.update(Entry(), validated_data)
     
        
    def update(self, instance, validated_data):
        #pre: Entry Instance and validated data
        #post: Entry information updated
    
        instance.datetime = validated_data.get('datetime')
        instance.amount = validated_data.get('amount')
        instance.concept = validated_data.get('concept')
            
        instance.save()
        return instance
    
    
    #override udatetime field
    #Can not be two Entries with the same datetime
    def validate_datetime(self, data):
        date = Entry.objects.filter(datetime=data)
        try: 
            #Exist an entry
            if date:
                #Not the same instance  
                if self.instance.datetime!=data: 
                    raise ValueError("Entry already exists")
            #Incorrect datetime
            if (self.instance.datetime.strftime("%Y-%m-%d") < datetime.now().strftime("%Y-%m-%d") ) : 
                raise ValueError("Datetime incorrect")
        
        except ValueError as e: 
                raise serializers.ValidationError(e)
        return data
    
    
    def validate_amount(self, data):
        try: 
            #amount not 0
            if float(data) == 0.0: 
                raise ValueError("Entry already exists")
        
        except ValueError as e: 
                raise serializers.ValidationError(e)
        return data
        